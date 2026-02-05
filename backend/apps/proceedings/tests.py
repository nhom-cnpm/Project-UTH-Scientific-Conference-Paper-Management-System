from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from .models import (
    Proceedings, ProceedingsEditor, ProceedingsEntry,
    Section, ExportHistory, Copyright
)
from .services import ProceedingsService
from accounts.models import User
from conferences.models import Conference
from submissions.models import Paper

# Create your tests here.

# ============================================
# MODEL TESTS
# ============================================

class ProceedingsModelTestCase(TestCase):
    """Test cases cho Proceedings model"""
    
    def setUp(self):
        """Setup test data"""
        # Create chair
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
            venue='Test',
            city='Test',
            country='Test',
            chair=self.chair,
        )
    
    def test_create_proceedings(self):
        """Test tạo proceedings thành công"""
        proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Proceedings of Test Conference 2026',
            isbn='978-3-16-148410-0',
            publisher='Springer',
            status='draft'
        )
        
        self.assertEqual(proceedings.conference, self.conference)
        self.assertEqual(proceedings.title, 'Proceedings of Test Conference 2026')
        self.assertEqual(proceedings.status, 'draft')
        self.assertFalse(proceedings.is_deleted)
    
    def test_proceedings_str_representation(self):
        """Test __str__ method"""
        proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Proceedings of TC 2026'
        )
        
        expected_str = f"Proceedings of TC 2026 ({self.conference.acronym})"
        self.assertEqual(str(proceedings), expected_str)
    
    def test_one_proceedings_per_conference(self):
        """Test một conference chỉ có 1 proceedings"""
        Proceedings.objects.create(
            conference=self.conference,
            title='First Proceedings'
        )
        
        # Try to create second proceedings for same conference
        with self.assertRaises(Exception):
            Proceedings.objects.create(
                conference=self.conference,
                title='Second Proceedings'
            )
    
    def test_publication_date_validation(self):
        """Test validation: publication date phải sau conference end date"""
        proceedings = Proceedings(
            conference=self.conference,
            title='Test Proceedings',
            publication_date=self.conference.start_date - timedelta(days=1)
        )
        
        with self.assertRaises(ValidationError):
            proceedings.clean()
    
    def test_publish_proceedings(self):
        """Test publish proceedings"""
        proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Test Proceedings',
            status='in_preparation',
            full_proceedings_pdf=SimpleUploadedFile("proceedings.pdf", b"content")
        )
        
        # Should be in_preparation
        self.assertEqual(proceedings.status, 'in_preparation')
        self.assertIsNone(proceedings.published_at)
        
        # Publish
        proceedings.publish()
        
        self.assertEqual(proceedings.status, 'published')
        self.assertIsNotNone(proceedings.published_at)
    
    def test_cannot_publish_without_pdf(self):
        """Test không thể publish thiếu PDF"""
        proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Test Proceedings',
            status='in_preparation',
            # No PDF file
        )
        
        with self.assertRaises(ValidationError):
            proceedings.publish()
    
    def test_cannot_publish_from_draft(self):
        """Test không thể publish từ draft status"""
        proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Test Proceedings',
            status='draft',
            full_proceedings_pdf=SimpleUploadedFile("proceedings.pdf", b"content")
        )
        
        with self.assertRaises(ValidationError):
            proceedings.publish()
    
    def test_calculate_statistics(self):
        """Test tính statistics"""
        proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        # Create dummy papers and entries
        author = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123'
        )
        
        for i in range(3):
            paper = Paper.objects.create(
                conference=self.conference,
                submitter=author,
                title=f'Paper {i+1}',
                abstract='Abstract',
                pdf_file=SimpleUploadedFile(f"paper{i}.pdf", b"content"),
                status='accepted'
            )
            
            ProceedingsEntry.objects.create(
                proceedings=proceedings,
                paper=paper,
                page_start=i * 10 + 1,
                page_end=i * 10 + 10,
                is_included=True
            )
        
        # Calculate statistics
        proceedings.calculate_statistics()
        
        self.assertEqual(proceedings.total_papers, 3)
        self.assertEqual(proceedings.total_pages, 30)  # 3 papers x 10 pages


class ProceedingsEditorModelTestCase(TestCase):
    """Test cases cho ProceedingsEditor"""
    
    def setUp(self):
        """Setup test data"""
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
        
        self.proceedings = Proceedings.objects.create(
            conference=conference,
            title='Test Proceedings'
        )
        
        self.editor = User.objects.create_user(
            email='editor@example.com',
            username='editor',
            password='pass123',
            full_name='Chief Editor'
        )
    
    def test_create_proceedings_editor(self):
        """Test tạo proceedings editor"""
        editor_assignment = ProceedingsEditor.objects.create(
            proceedings=self.proceedings,
            editor=self.editor,
            role='Chief Editor',
            order=1
        )
        
        self.assertEqual(editor_assignment.proceedings, self.proceedings)
        self.assertEqual(editor_assignment.editor, self.editor)
        self.assertEqual(editor_assignment.role, 'Chief Editor')
    
    def test_unique_editor_per_proceedings(self):
        """Test một editor chỉ xuất hiện 1 lần trong proceedings"""
        ProceedingsEditor.objects.create(
            proceedings=self.proceedings,
            editor=self.editor,
            role='Chief Editor'
        )
        
        # Try to add same editor again
        with self.assertRaises(Exception):
            ProceedingsEditor.objects.create(
                proceedings=self.proceedings,
                editor=self.editor,
                role='Associate Editor'
            )
    
    def test_editor_ordering(self):
        """Test ordering của editors"""
        editor2 = User.objects.create_user(
            email='editor2@example.com',
            username='editor2',
            password='pass123'
        )
        
        ProceedingsEditor.objects.create(
            proceedings=self.proceedings,
            editor=editor2,
            order=2
        )
        
        ProceedingsEditor.objects.create(
            proceedings=self.proceedings,
            editor=self.editor,
            order=1
        )
        
        editors = self.proceedings.editor_assignments.all()
        
        # Should be ordered by order field
        self.assertEqual(editors[0].order, 1)
        self.assertEqual(editors[1].order, 2)


class ProceedingsEntryModelTestCase(TestCase):
    """Test cases cho ProceedingsEntry"""
    
    def setUp(self):
        """Setup test data"""
        self.author = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123'
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
        
        self.proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Test Proceedings',
            doi_prefix='10.1234'
        )
        
        self.paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.author,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content"),
            status='accepted'
        )
    
    def test_create_proceedings_entry(self):
        """Test tạo proceedings entry"""
        entry = ProceedingsEntry.objects.create(
            proceedings=self.proceedings,
            paper=self.paper,
            page_start=1,
            page_end=10,
            section='Machine Learning',
            display_order=1
        )
        
        self.assertEqual(entry.proceedings, self.proceedings)
        self.assertEqual(entry.paper, self.paper)
        self.assertTrue(entry.is_included)
    
    def test_only_accepted_papers_can_be_added(self):
        """Test chỉ accepted papers mới được thêm vào proceedings"""
        draft_paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.author,
            title='Draft Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("draft.pdf", b"content"),
            status='draft'
        )
        
        entry = ProceedingsEntry(
            proceedings=self.proceedings,
            paper=draft_paper,
            page_start=1,
            page_end=10
        )
        
        with self.assertRaises(ValidationError):
            entry.clean()
    
    def test_page_end_must_be_after_page_start(self):
        """Test page_end phải >= page_start"""
        entry = ProceedingsEntry(
            proceedings=self.proceedings,
            paper=self.paper,
            page_start=10,
            page_end=5  # Invalid
        )
        
        with self.assertRaises(ValidationError):
            entry.clean()
    
    def test_page_count_property(self):
        """Test page_count property"""
        entry = ProceedingsEntry.objects.create(
            proceedings=self.proceedings,
            paper=self.paper,
            page_start=1,
            page_end=10
        )
        
        self.assertEqual(entry.page_count, 10)
    
    def test_page_count_without_pages(self):
        """Test page_count khi chưa có page numbers"""
        entry = ProceedingsEntry.objects.create(
            proceedings=self.proceedings,
            paper=self.paper
        )
        
        self.assertEqual(entry.page_count, 0)
    
    def test_generate_doi(self):
        """Test generate DOI"""
        entry = ProceedingsEntry.objects.create(
            proceedings=self.proceedings,
            paper=self.paper,
            page_start=1,
            page_end=10
        )
        
        doi = entry.generate_doi()
        
        self.assertIsNotNone(doi)
        self.assertIn('10.1234', doi)
        self.assertIn(str(self.conference.start_date.year), doi)
    
    def test_generate_doi_without_prefix(self):
        """Test generate DOI khi không có prefix"""
        proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='No DOI Proceedings',
            doi_prefix=''  # No prefix
        )
        
        entry = ProceedingsEntry.objects.create(
            proceedings=proceedings,
            paper=self.paper
        )
        
        doi = entry.generate_doi()
        
        self.assertIsNone(doi)
    
    def test_unique_paper_per_proceedings(self):
        """Test một paper chỉ xuất hiện 1 lần trong proceedings"""
        ProceedingsEntry.objects.create(
            proceedings=self.proceedings,
            paper=self.paper,
            page_start=1,
            page_end=10
        )
        
        # Try to add same paper again
        with self.assertRaises(Exception):
            ProceedingsEntry.objects.create(
                proceedings=self.proceedings,
                paper=self.paper,
                page_start=11,
                page_end=20
            )


class SectionModelTestCase(TestCase):
    """Test cases cho Section"""
    
    def setUp(self):
        """Setup test data"""
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
        
        self.proceedings = Proceedings.objects.create(
            conference=conference,
            title='Test Proceedings'
        )
    
    def test_create_section(self):
        """Test tạo section"""
        section = Section.objects.create(
            proceedings=self.proceedings,
            name='Machine Learning',
            description='ML papers',
            order=1
        )
        
        self.assertEqual(section.name, 'Machine Learning')
        self.assertEqual(section.proceedings, self.proceedings)
    
    def test_unique_section_name_per_proceedings(self):
        """Test section name phải unique trong proceedings"""
        Section.objects.create(
            proceedings=self.proceedings,
            name='AI',
            order=1
        )
        
        # Try to create another section with same name
        with self.assertRaises(Exception):
            Section.objects.create(
                proceedings=self.proceedings,
                name='AI',
                order=2
            )
    
    def test_section_ordering(self):
        """Test ordering của sections"""
        Section.objects.create(proceedings=self.proceedings, name='Section B', order=2)
        Section.objects.create(proceedings=self.proceedings, name='Section A', order=1)
        
        sections = self.proceedings.sections.all()
        
        # Should be ordered by order field
        self.assertEqual(sections[0].name, 'Section A')
        self.assertEqual(sections[1].name, 'Section B')


class CopyrightModelTestCase(TestCase):
    """Test cases cho Copyright"""
    
    def setUp(self):
        """Setup test data"""
        author = User.objects.create_user(
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
        
        proceedings = Proceedings.objects.create(
            conference=conference,
            title='Test Proceedings'
        )
        
        paper = Paper.objects.create(
            conference=conference,
            submitter=author,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content"),
            status='accepted'
        )
        
        self.entry = ProceedingsEntry.objects.create(
            proceedings=proceedings,
            paper=paper
        )
    
    def test_create_copyright(self):
        """Test tạo copyright info"""
        copyright_info = Copyright.objects.create(
            entry=self.entry,
            copyright_holder='The Authors',
            copyright_year=2026,
            license_type='CC BY 4.0',
            copyright_form_signed=True
        )
        
        self.assertEqual(copyright_info.copyright_holder, 'The Authors')
        self.assertEqual(copyright_info.copyright_year, 2026)
        self.assertTrue(copyright_info.copyright_form_signed)


# ============================================
# SERVICE TESTS
# ============================================

class ProceedingsServiceTestCase(TestCase):
    """Test cases cho ProceedingsService"""
    
    def setUp(self):
        """Setup test data"""
        self.chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            status='active'
        )
        
        self.author = User.objects.create_user(
            email='author@example.com',
            username='author',
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
            chair=self.chair,
        )
    
    def test_create_proceedings_service(self):
        """Test tạo proceedings qua service"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Proceedings of TC 2026',
            publisher='Springer'
        )
        
        self.assertIsNotNone(proceedings)
        self.assertEqual(proceedings.conference, self.conference)
        self.assertEqual(proceedings.title, 'Proceedings of TC 2026')
    
    def test_cannot_create_duplicate_proceedings(self):
        """Test không thể tạo 2 proceedings cho 1 conference"""
        ProceedingsService.create_proceedings(
            conference=self.conference,
            title='First Proceedings'
        )
        
        with self.assertRaises(ValidationError):
            ProceedingsService.create_proceedings(
                conference=self.conference,
                title='Second Proceedings'
            )
    
    def test_add_paper_service(self):
        """Test thêm paper vào proceedings"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.author,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content"),
            status='accepted'
        )
        
        entry = ProceedingsService.add_paper(
            proceedings=proceedings,
            paper=paper,
            page_start=1,
            page_end=10
        )
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.paper, paper)
    
    def test_cannot_add_non_accepted_paper(self):
        """Test không thể thêm paper chưa accept"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        draft_paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.author,
            title='Draft Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("draft.pdf", b"content"),
            status='draft'
        )
        
        with self.assertRaises(ValidationError):
            ProceedingsService.add_paper(
                proceedings=proceedings,
                paper=draft_paper
            )
    
    def test_remove_paper_service(self):
        """Test xóa paper khỏi proceedings"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.author,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content"),
            status='accepted'
        )
        
        # Add paper
        ProceedingsService.add_paper(proceedings, paper)
        
        # Remove paper
        result = ProceedingsService.remove_paper(proceedings, paper)
        
        self.assertTrue(result)
        self.assertFalse(
            ProceedingsEntry.objects.filter(
                proceedings=proceedings,
                paper=paper
            ).exists()
        )
    
    def test_generate_table_of_contents(self):
        """Test generate table of contents"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        # Add multiple papers
        for i in range(3):
            paper = Paper.objects.create(
                conference=self.conference,
                submitter=self.author,
                title=f'Paper {i+1}',
                abstract='Abstract',
                pdf_file=SimpleUploadedFile(f"paper{i}.pdf", b"content"),
                status='accepted'
            )
            
            ProceedingsService.add_paper(
                proceedings,
                paper,
                page_start=i * 10 + 1,
                page_end=i * 10 + 10
            )
        
        toc = ProceedingsService.generate_table_of_contents(proceedings)
        
        self.assertEqual(len(toc), 3)
        self.assertIn('title', toc[0])
        self.assertIn('pages', toc[0])
    
    def test_assign_page_numbers(self):
        """Test tự động assign page numbers"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        # Add papers without page numbers
        for i in range(3):
            paper = Paper.objects.create(
                conference=self.conference,
                submitter=self.author,
                title=f'Paper {i+1}',
                abstract='Abstract',
                pdf_file=SimpleUploadedFile(f"paper{i}.pdf", b"content"),
                status='accepted'
            )
            
            ProceedingsService.add_paper(
                proceedings,
                paper,
                display_order=i + 1
            )
        
        # Assign page numbers
        ProceedingsService.assign_page_numbers(proceedings, start_page=1)
        
        # Verify pages assigned
        entries = proceedings.entries.all().order_by('display_order')
        self.assertIsNotNone(entries[0].page_start)
        self.assertIsNotNone(entries[0].page_end)
    
    def test_publish_proceedings_service(self):
        """Test publish proceedings"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        proceedings.status = 'in_preparation'
        proceedings.full_proceedings_pdf = SimpleUploadedFile("proc.pdf", b"content")
        proceedings.save()
        
        # Add a paper
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=self.author,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content"),
            status='accepted'
        )
        
        ProceedingsService.add_paper(proceedings, paper)
        
        # Set DOI prefix
        proceedings.doi_prefix = '10.1234'
        proceedings.save()
        
        # Publish
        result = ProceedingsService.publish_proceedings(proceedings)
        
        self.assertEqual(result.status, 'published')
        
        # Check DOI generated
        entry = proceedings.entries.first()
        self.assertIsNotNone(entry.doi)
    
    def test_create_section_service(self):
        """Test tạo section"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        section = ProceedingsService.create_section(
            proceedings=proceedings,
            name='Machine Learning',
            order=1,
            description='ML papers'
        )
        
        self.assertIsNotNone(section)
        self.assertEqual(section.name, 'Machine Learning')
    
    def test_organize_by_sections(self):
        """Test organize entries by sections"""
        proceedings = ProceedingsService.create_proceedings(
            conference=self.conference,
            title='Test Proceedings'
        )
        
        # Create sections
        ProceedingsService.create_section(
            proceedings, 'AI', 1
        )
        ProceedingsService.create_section(
            proceedings, 'ML', 2
        )
        
        # Add papers
        for i in range(2):
            paper = Paper.objects.create(
                conference=self.conference,
                submitter=self.author,
                title=f'AI Paper {i+1}',
                abstract='Abstract',
                pdf_file=SimpleUploadedFile(f"ai{i}.pdf", b"content"),
                status='accepted'
            )
            
            ProceedingsService.add_paper(
                proceedings,
                paper,
                section='AI'
            )
        
        organized = ProceedingsService.organize_by_sections(proceedings)
        
        self.assertIsInstance(organized, list)
        self.assertGreater(len(organized), 0)


# ============================================
# API TESTS
# ============================================

class ProceedingsAPITestCase(APITestCase):
    """Test cases cho Proceedings APIs"""
    
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        
        # Create chair
        self.chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            full_name='Program Chair',
            status='active',
            is_staff=True  # Make admin for testing
        )
        
        # Create normal user
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
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
            chair=self.chair,
        )
        
        # Create proceedings
        self.proceedings = Proceedings.objects.create(
            conference=self.conference,
            title='Proceedings of TC 2026',
            doi_prefix='10.1234'
        )
        
        self.list_url = reverse('proceedings-list')
        self.detail_url = reverse('proceedings-detail', args=[self.proceedings.proceedings_id])
    
    def test_list_proceedings(self):
        """Test lấy danh sách proceedings"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_table_of_contents(self):
        """Test lấy table of contents"""
        self.client.force_authenticate(user=self.user)
        
        # Add a paper
        author = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123'
        )
        
        paper = Paper.objects.create(
            conference=self.conference,
            submitter=author,
            title='Test Paper',
            abstract='Abstract',
            pdf_file=SimpleUploadedFile("test.pdf", b"content"),
            status='accepted'
        )
        
        ProceedingsEntry.objects.create(
            proceedings=self.proceedings,
            paper=paper,
            page_start=1,
            page_end=10
        )
        
        url = reverse('proceedings-table-of-contents', args=[self.proceedings.proceedings_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('entries', response.data)
    
    def test_publish_proceedings_api(self):
        """Test publish proceedings qua API"""
        self.client.force_authenticate(user=self.chair)
        
        # Prepare proceedings
        self.proceedings.status = 'in_preparation'
        self.proceedings.full_proceedings_pdf = SimpleUploadedFile("proc.pdf", b"content")
        self.proceedings.save()
        
        url = reverse('proceedings-publish', args=[self.proceedings.proceedings_id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify published
        self.proceedings.refresh_from_db()
        self.assertEqual(self.proceedings.status, 'published')
    
    def test_only_chair_can_publish(self):
        """Test chỉ chair mới có thể publish"""
        self.client.force_authenticate(user=self.user)
        
        self.proceedings.status = 'in_preparation'
        self.proceedings.full_proceedings_pdf = SimpleUploadedFile("proc.pdf", b"content")
        self.proceedings.save()
        
        url = reverse('proceedings-publish', args=[self.proceedings.proceedings_id])
        response = self.client.post(url)
        
        # Should fail
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_statistics(self):
        """Test lấy statistics"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('proceedings-statistics', args=[self.proceedings.proceedings_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_papers', response.data)
        self.assertIn('total_pages', response.data)


# ============================================
# INTEGRATION TESTS
# ============================================

class ProceedingsWorkflowTestCase(APITestCase):
    """Test complete proceedings workflow"""
    
    def test_complete_proceedings_workflow(self):
        """
        Test complete workflow:
        1. Create conference
        2. Create proceedings
        3. Add papers
        4. Create sections
        5. Assign page numbers
        6. Generate DOIs
        7. Publish
        """
        # 1. Create conference
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            status='active'
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
        )
        
        # 2. Create proceedings
        proceedings = ProceedingsService.create_proceedings(
            conference=conference,
            title='Proceedings of WTC 2026',
            doi_prefix='10.9999'
        )
        
        self.assertIsNotNone(proceedings)
        
        # 3. Add papers
        author = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='pass123'
        )
        
        for i in range(3):
            paper = Paper.objects.create(
                conference=conference,
                submitter=author,
                title=f'Workflow Paper {i+1}',
                abstract='Abstract',
                pdf_file=SimpleUploadedFile(f"paper{i}.pdf", b"content"),
                status='accepted'
            )
            
            ProceedingsService.add_paper(
                proceedings,
                paper,
                section='AI' if i < 2 else 'ML',
                display_order=i + 1
            )
        
        self.assertEqual(proceedings.entries.count(), 3)
        
        # 4. Create sections
        ProceedingsService.create_section(proceedings, 'AI', 1)
        ProceedingsService.create_section(proceedings, 'ML', 2)
        
        self.assertEqual(proceedings.sections.count(), 2)
        
        # 5. Assign page numbers
        ProceedingsService.assign_page_numbers(proceedings)
        
        # 6. Prepare for publication
        proceedings.status = 'in_preparation'
        proceedings.full_proceedings_pdf = SimpleUploadedFile("final.pdf", b"content")
        proceedings.save()
        
        # 7. Publish
        ProceedingsService.publish_proceedings(proceedings)
        
        proceedings.refresh_from_db()
        self.assertEqual(proceedings.status, 'published')
        
        # Verify DOIs generated
        for entry in proceedings.entries.all():
            self.assertIsNotNone(entry.doi)