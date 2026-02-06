from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from .models import (
    Paper, PaperAuthor, PaperVersion, 
    CameraReadySubmission, Metadata, SubmissionActivity
)
from .services import PaperService
from accounts.models import User
from conferences.models import Conference, Track, Topic

# Create your tests here.

class PaperModelTestCase(TestCase):
    """Test cases cho Paper model"""
    
    def setUp(self):
        """Setup test data"""
        # Create users
        self.submitter = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123',
            full_name='Test Author',
            status='active'
        )
        
        self.chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            full_name='Program Chair',
            status='active'
        )
        
        # Create conference
        self.conference = Conference.objects.create(
            name='Test Conference',
            acronym='TC',
            description='Test',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Test Venue',
            city='Test City',
            country='Test Country',
            chair=self.chair,
            status='open'  # Open for submission
        )
        
        # Create dummy PDF file
        self.pdf_file = SimpleUploadedFile(
            "test_paper.pdf",
            b"file_content",
            content_type="application/pdf"
        )
    
    def test_create_paper(self):
        """Test tạo paper thành công"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='This is a test abstract',
            keywords='machine learning, AI',
            pdf_file=self.pdf_file,
            status='draft'
        )
        
        self.assertEqual(paper.title, 'Test Paper')
        self.assertEqual(paper.submitter, self.submitter)
        self.assertEqual(paper.status, 'draft')
        self.assertFalse(paper.is_deleted)
    
    def test_paper_str_representation(self):
        """Test __str__ method"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='A Very Long Paper Title That Should Be Truncated In String Representation',
            abstract='Abstract',
            pdf_file=self.pdf_file
        )
        
        str_repr = str(paper)
        self.assertIn('draft', str_repr.lower())
        self.assertLessEqual(len(str_repr), 100)
    
    def test_paper_submit(self):
        """Test submit paper"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='draft'
        )
        
        # Add at least one author
        PaperAuthor.objects.create(
            paper=paper,
            author=self.submitter,
            order=1
        )
        
        # Should be in draft status
        self.assertEqual(paper.status, 'draft')
        self.assertIsNone(paper.submitted_at)
        
        # Submit
        paper.submit()
        
        self.assertEqual(paper.status, 'submitted')
        self.assertIsNotNone(paper.submitted_at)
    
    def test_cannot_submit_without_authors(self):
        """Test không thể submit paper không có author"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='draft'
        )
        
        with self.assertRaises(ValidationError):
            paper.submit()
    
    def test_cannot_submit_without_required_fields(self):
        """Test không thể submit thiếu thông tin"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='',  # Empty title
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='draft'
        )
        
        PaperAuthor.objects.create(
            paper=paper,
            author=self.submitter,
            order=1
        )
        
        with self.assertRaises(ValidationError):
            paper.submit()
    
    def test_cannot_submit_twice(self):
        """Test không thể submit 2 lần"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='draft'
        )
        
        PaperAuthor.objects.create(
            paper=paper,
            author=self.submitter,
            order=1
        )
        
        # Submit first time
        paper.submit()
        
        # Try to submit again
        with self.assertRaises(ValidationError):
            paper.submit()
    
    def test_withdraw_paper(self):
        """Test withdraw paper"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='submitted'
        )
        
        paper.withdraw()
        
        self.assertEqual(paper.status, 'withdrawn')
    
    def test_accept_paper(self):
        """Test accept paper"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='under_review'
        )
        
        paper.accept()
        
        self.assertEqual(paper.status, 'accepted')
    
    def test_reject_paper(self):
        """Test reject paper"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='under_review'
        )
        
        paper.reject()
        
        self.assertEqual(paper.status, 'rejected')
    
    def test_request_revision(self):
        """Test request revision"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='under_review'
        )
        
        paper.request_revision()
        
        self.assertEqual(paper.status, 'revision_requested')
    
    def test_is_editable(self):
        """Test kiểm tra paper có thể edit không"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file,
            status='draft'
        )
        
        # Draft should be editable
        self.assertTrue(paper.is_editable())
        
        # Submitted should not be editable
        paper.status = 'submitted'
        paper.save()
        self.assertFalse(paper.is_editable())
        
        # Revision requested should be editable
        paper.status = 'revision_requested'
        paper.save()
        self.assertTrue(paper.is_editable())
    
    def test_author_list_property(self):
        """Test author_list property"""
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=self.pdf_file
        )
        
        # Add authors
        author2 = User.objects.create_user(
            email='author2@example.com',
            username='author2',
            password='pass123',
            full_name='Second Author'
        )
        
        PaperAuthor.objects.create(paper=paper, author=self.submitter, order=1)
        PaperAuthor.objects.create(paper=paper, author=author2, order=2)
        
        author_list = paper.author_list
        self.assertIn('Test Author', author_list)
        self.assertIn('Second Author', author_list)


class PaperAuthorModelTestCase(TestCase):
    """Test cases cho PaperAuthor model"""
    
    def setUp(self):
        """Setup test data"""
        self.submitter = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123',
            full_name='Test Author'
        )
        
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123'
        )
        
        self.conference = Conference.objects.create(
            name='Test Conference',
            acronym='TC',
            description='Test',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Test',
            city='Test',
            country='Test',
            chair=chair,
        )
        
        self.paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content")
        )
    
    def test_create_paper_author(self):
        """Test tạo paper author"""
        paper_author = PaperAuthor.objects.create(
            paper=self.paper,
            author=self.submitter,
            order=1,
            is_corresponding=True
        )
        
        self.assertEqual(paper_author.paper, self.paper)
        self.assertEqual(paper_author.author, self.submitter)
        self.assertEqual(paper_author.order, 1)
        self.assertTrue(paper_author.is_corresponding)
    
    def test_unique_paper_author_constraint(self):
        """Test một author chỉ xuất hiện 1 lần trong paper"""
        PaperAuthor.objects.create(
            paper=self.paper,
            author=self.submitter,
            order=1
        )
        
        # Try to add same author again
        with self.assertRaises(Exception):
            PaperAuthor.objects.create(
                paper=self.paper,
                author=self.submitter,
                order=2
            )
    
    def test_author_ordering(self):
        """Test ordering của authors"""
        author2 = User.objects.create_user(
            email='author2@example.com',
            username='author2',
            password='pass123'
        )
        
        PaperAuthor.objects.create(paper=self.paper, author=author2, order=2)
        PaperAuthor.objects.create(paper=self.paper, author=self.submitter, order=1)
        
        authors = self.paper.paper_authors.all()
        
        # Should be ordered by order field
        self.assertEqual(authors[0].order, 1)
        self.assertEqual(authors[1].order, 2)


class PaperVersionModelTestCase(TestCase):
    """Test cases cho PaperVersion"""
    
    def setUp(self):
        """Setup test data"""
        submitter = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123'
        )
        
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123'
        )
        
        conference = Conference.objects.create(
            name='Test Conference',
            acronym='TC',
            description='Test',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Test',
            city='Test',
            country='Test',
            chair=chair,
        )
        
        self.paper = Paper.objects.create(
            conference=conference,
            submitter=submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content")
        )
        
        self.submitter = submitter
    
    def test_create_paper_version(self):
        """Test tạo paper version"""
        version = PaperVersion.objects.create(
            paper=self.paper,
            version_number=1,
            pdf_file=SimpleUploadedFile("test_v1.pdf", b"content"),
            changes_summary="Initial version",
            uploaded_by=self.submitter
        )
        
        self.assertEqual(version.version_number, 1)
        self.assertEqual(version.paper, self.paper)
    
    def test_unique_version_number_per_paper(self):
        """Test version number phải unique trong paper"""
        PaperVersion.objects.create(
            paper=self.paper,
            version_number=1,
            pdf_file=SimpleUploadedFile("test_v1.pdf", b"content"),
            uploaded_by=self.submitter
        )
        
        # Try to create another version with same number
        with self.assertRaises(Exception):
            PaperVersion.objects.create(
                paper=self.paper,
                version_number=1,
                pdf_file=SimpleUploadedFile("test_v1_dup.pdf", b"content"),
                uploaded_by=self.submitter
            )
    
    def test_version_ordering(self):
        """Test versions được sắp xếp theo version_number giảm dần"""
        PaperVersion.objects.create(
            paper=self.paper,
            version_number=1,
            pdf_file=SimpleUploadedFile("v1.pdf", b"v1"),
            uploaded_by=self.submitter
        )
        
        PaperVersion.objects.create(
            paper=self.paper,
            version_number=2,
            pdf_file=SimpleUploadedFile("v2.pdf", b"v2"),
            uploaded_by=self.submitter
        )
        
        versions = self.paper.versions.all()
        
        # Should be ordered by version_number descending
        self.assertEqual(versions[0].version_number, 2)
        self.assertEqual(versions[1].version_number, 1)


class MetadataModelTestCase(TestCase):
    """Test cases cho Metadata"""
    
    def setUp(self):
        """Setup test data"""
        submitter = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123'
        )
        
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123'
        )
        
        conference = Conference.objects.create(
            name='Test Conference',
            acronym='TC',
            description='Test',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Test',
            city='Test',
            country='Test',
            chair=chair,
        )
        
        self.paper = Paper.objects.create(
            conference=conference,
            submitter=submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content")
        )
    
    def test_create_metadata(self):
        """Test tạo metadata"""
        metadata = Metadata.objects.create(
            paper=self.paper,
            paper_type='full',
            primary_area='Machine Learning',
            data_available=True,
            data_url='https://github.com/example/data',
            code_available=True,
            code_url='https://github.com/example/code'
        )
        
        self.assertEqual(metadata.paper, self.paper)
        self.assertEqual(metadata.paper_type, 'full')
        self.assertTrue(metadata.data_available)
        self.assertTrue(metadata.code_available)


# ============================================
# SERVICE TESTS
# ============================================

class PaperServiceTestCase(TestCase):
    """Test cases cho PaperService"""
    
    def setUp(self):
        """Setup test data"""
        self.submitter = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123',
            full_name='Test Author',
            status='active'
        )
        
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123'
        )
        
        self.conference = Conference.objects.create(
            name='Test Conference',
            acronym='TC',
            description='Test',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Test',
            city='Test',
            country='Test',
            chair=chair,
            status='open'
        )
    
    def test_create_paper_service(self):
        """Test tạo paper qua service"""
        paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper via Service',
            abstract='Test abstract',
            keywords='AI, ML'
        )
        
        self.assertIsNotNone(paper)
        self.assertEqual(paper.title, 'Test Paper via Service')
        self.assertEqual(paper.submitter, self.submitter)
        
        # Should auto-add submitter as first author
        self.assertTrue(
            PaperAuthor.objects.filter(
                paper=paper,
                author=self.submitter,
                order=1
            ).exists()
        )
        
        # Should log activity
        self.assertTrue(
            SubmissionActivity.objects.filter(
                paper=paper,
                activity_type='created'
            ).exists()
        )
    
    def test_cannot_create_paper_when_conference_closed(self):
        """Test không thể tạo paper khi conference đóng"""
        # Close conference
        self.conference.status = 'review'
        self.conference.save()
        
        with self.assertRaises(ValidationError):
            PaperService.create_paper(
                conference=self.conference,
                submitter=self.submitter,
                title='Test Paper',
                abstract='Abstract'
            )
    
    def test_submit_paper_service(self):
        """Test submit paper qua service"""
        paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content")
        )
        
        # Submit
        result = PaperService.submit_paper(paper, self.submitter)
        
        self.assertEqual(result.status, 'submitted')
        self.assertIsNotNone(result.submitted_at)
    
    def test_add_author_service(self):
        """Test thêm author qua service"""
        paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract'
        )
        
        # Add second author
        author2 = User.objects.create_user(
            email='author2@example.com',
            username='author2',
            password='pass123',
            full_name='Second Author'
        )
        
        paper_author = PaperService.add_author(paper, author2, order=2)
        
        self.assertIsNotNone(paper_author)
        self.assertEqual(paper_author.order, 2)
        
        # Should log activity
        self.assertTrue(
            SubmissionActivity.objects.filter(
                paper=paper,
                activity_type='author_added'
            ).exists()
        )
    
    def test_cannot_add_duplicate_author(self):
        """Test không thể thêm author trùng"""
        paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract'
        )
        
        # Try to add submitter again (already added as first author)
        with self.assertRaises(ValidationError):
            PaperService.add_author(paper, self.submitter, order=2)
    
    def test_remove_author_service(self):
        """Test xóa author qua service"""
        paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract'
        )
        
        # Add second author
        author2 = User.objects.create_user(
            email='author2@example.com',
            username='author2',
            password='pass123'
        )
        PaperService.add_author(paper, author2, order=2)
        
        # Remove second author
        result = PaperService.remove_author(paper, author2)
        
        self.assertTrue(result)
        self.assertFalse(
            PaperAuthor.objects.filter(paper=paper, author=author2).exists()
        )
    
    def test_cannot_remove_only_author(self):
        """Test không thể xóa author duy nhất"""
        paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract'
        )
        
        # Try to remove the only author
        with self.assertRaises(ValidationError):
            PaperService.remove_author(paper, self.submitter)
    
    def test_upload_new_version_service(self):
        """Test upload version mới"""
        paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("v1.pdf", b"v1")
        )
        
        # Upload new version
        new_file = SimpleUploadedFile("v2.pdf", b"v2")
        version = PaperService.upload_new_version(
            paper, new_file, self.submitter, "Fixed typos"
        )
        
        self.assertIsNotNone(version)
        self.assertEqual(version.version_number, 1)
        self.assertEqual(version.changes_summary, "Fixed typos")
    
    def test_get_user_papers(self):
        """Test lấy papers của user"""
        # Create multiple papers
        for i in range(3):
            PaperService.create_paper(
                conference=self.conference,
                submitter=self.submitter,
                title=f'Paper {i+1}',
                abstract='Abstract'
            )
        
        papers = PaperService.get_user_papers(self.submitter)
        
        self.assertEqual(papers.count(), 3)
    
    def test_get_conference_papers(self):
        """Test lấy papers của conference"""
        # Create papers from different users
        for i in range(2):
            user = User.objects.create_user(
                email=f'user{i}@example.com',
                username=f'user{i}',
                password='pass123'
            )
            PaperService.create_paper(
                conference=self.conference,
                submitter=user,
                title=f'Paper {i+1}',
                abstract='Abstract'
            )
        
        papers = PaperService.get_conference_papers(self.conference)
        
        self.assertEqual(papers.count(), 2)


# ============================================
# API TESTS
# ============================================

class PaperAPITestCase(APITestCase):
    """Test cases cho Paper APIs"""
    
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        
        # Create users
        self.submitter = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123',
            full_name='Test Author',
            status='active'
        )
        
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='other',
            password='pass123',
            status='active'
        )
        
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            status='active'
        )
        
        # Create conference
        self.conference = Conference.objects.create(
            name='Test Conference',
            acronym='TC',
            description='Test',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Test',
            city='Test',
            country='Test',
            chair=chair,
            status='open'
        )
        
        # Create paper
        self.paper = PaperService.create_paper(
            conference=self.conference,
            submitter=self.submitter,
            title='Test Paper',
            abstract='Test abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content")
        )
        
        self.list_url = reverse('paper-list')
        self.detail_url = reverse('paper-detail', args=[self.paper.paper_id])
    
    def test_get_my_papers(self):
        """Test lấy papers của user hiện tại"""
        self.client.force_authenticate(user=self.submitter)
        
        url = reverse('paper-my-papers')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_user_can_only_see_own_papers(self):
        """Test user chỉ thấy papers của mình"""
        self.client.force_authenticate(user=self.other_user)
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Other user should not see submitter's paper
        self.assertEqual(len(response.data), 0)
    
    def test_submit_paper_api(self):
        """Test submit paper qua API"""
        self.client.force_authenticate(user=self.submitter)
        
        url = reverse('paper-submit', args=[self.paper.paper_id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify status changed
        self.paper.refresh_from_db()
        self.assertEqual(self.paper.status, 'submitted')
    
    def test_only_submitter_can_submit(self):
        """Test chỉ submitter mới có thể submit"""
        self.client.force_authenticate(user=self.other_user)
        
        url = reverse('paper-submit', args=[self.paper.paper_id])
        response = self.client.post(url)
        
        # Should fail because other_user is not the submitter
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    
    def test_withdraw_paper_api(self):
        """Test withdraw paper"""
        # First submit the paper
        self.paper.status = 'submitted'
        self.paper.submitted_at = timezone.now()
        self.paper.save()
        
        self.client.force_authenticate(user=self.submitter)
        
        url = reverse('paper-withdraw', args=[self.paper.paper_id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify status changed
        self.paper.refresh_from_db()
        self.assertEqual(self.paper.status, 'withdrawn')
    
    def test_add_author_api(self):
        """Test thêm author qua API"""
        self.client.force_authenticate(user=self.submitter)
        
        url = reverse('paper-add-author', args=[self.paper.paper_id])
        data = {
            'author_id': self.other_user.id,
            'order': 2,
            'is_corresponding': False
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify author added
        self.assertTrue(
            PaperAuthor.objects.filter(
                paper=self.paper,
                author=self.other_user
            ).exists()
        )
    
    def test_filter_papers_by_conference(self):
        """Test filter papers theo conference"""
        self.client.force_authenticate(user=self.submitter)
        
        response = self.client.get(
            self.list_url,
            {'conference': self.conference.conference_id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_papers_by_status(self):
        """Test filter papers theo status"""
        self.client.force_authenticate(user=self.submitter)
        
        response = self.client.get(
            self.list_url,
            {'status': 'draft'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_papers(self):
        """Test search papers"""
        self.client.force_authenticate(user=self.submitter)
        
        response = self.client.get(
            self.list_url,
            {'search': 'Test'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================
# INTEGRATION TESTS
# ============================================

class PaperSubmissionWorkflowTestCase(APITestCase):
    """Test complete paper submission workflow"""
    
    def test_complete_submission_workflow(self):
        """
        Test complete workflow:
        1. Create paper
        2. Add authors
        3. Upload file
        4. Submit paper
        5. Upload new version
        """
        # Create user
        user = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123',
            full_name='Test Author',
            status='active'
        )
        
        # Create conference
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123'
        )
        
        conference = Conference.objects.create(
            name='Workflow Test Conference',
            acronym='WTC',
            description='Test',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Test',
            city='Test',
            country='Test',
            chair=chair,
            status='open'
        )
        
        # 1. Create paper
        paper = PaperService.create_paper(
            conference=conference,
            submitter=user,
            title='Workflow Test Paper',
            abstract='Testing complete workflow',
            pdf_file=SimpleUploadedFile("test.pdf", b"content")
        )
        
        self.assertIsNotNone(paper)
        self.assertEqual(paper.status, 'draft')
        
        # 2. Add second author
        author2 = User.objects.create_user(
            email='author2@example.com',
            username='author2',
            password='pass123',
            full_name='Second Author'
        )
        
        PaperService.add_author(paper, author2, order=2)
        self.assertEqual(paper.authors.count(), 2)
        
        # 3. Submit paper
        PaperService.submit_paper(paper, user)
        paper.refresh_from_db()
        self.assertEqual(paper.status, 'submitted')
        
        # 4. Upload new version (after requesting revision)
        paper.status = 'revision_requested'
        paper.save()
        
        new_file = SimpleUploadedFile("test_v2.pdf", b"revised content")
        version = PaperService.upload_new_version(
            paper, new_file, user, "Addressed reviewer comments"
        )
        
        self.assertIsNotNone(version)
        self.assertEqual(version.version_number, 1)
        
        # Verify complete workflow logged
        activities = SubmissionActivity.objects.filter(paper=paper)
        self.assertGreater(activities.count(), 0)