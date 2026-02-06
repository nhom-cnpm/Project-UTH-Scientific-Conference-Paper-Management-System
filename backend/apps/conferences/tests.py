from django.test import TestCase

# Create your tests here.

"""
Test cases cho conferences app
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from .models import Conference, Track, Topic, ConferenceTrackTopic, PolicySetting, SystemLog
from accounts.models import User


# ============================================
# MODEL TESTS
# ============================================

class ConferenceModelTestCase(TestCase):
    """Test cases cho Conference model"""
    
    def setUp(self):
        """Setup test data"""
        self.chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            full_name='Program Chair',
            status='active'
        )
        
        self.conference_data = {
            'name': 'International Conference on Machine Learning',
            'acronym': 'ICML',
            'description': 'Leading conference in ML',
            'start_date': timezone.now().date() + timedelta(days=180),
            'end_date': timezone.now().date() + timedelta(days=183),
            'submission_deadline': timezone.now() + timedelta(days=90),
            'review_deadline': timezone.now() + timedelta(days=120),
            'camera_ready_deadline': timezone.now() + timedelta(days=150),
            'venue': 'Convention Center',
            'city': 'Vienna',
            'country': 'Austria',
            'chair': self.chair,
        }
    
    def test_create_conference(self):
        """Test tạo conference thành công"""
        conference = Conference.objects.create(**self.conference_data)
        
        self.assertEqual(conference.name, self.conference_data['name'])
        self.assertEqual(conference.acronym, self.conference_data['acronym'])
        self.assertEqual(conference.chair, self.chair)
        self.assertEqual(conference.status, 'draft')
        self.assertFalse(conference.is_deleted)
    
    def test_conference_str_representation(self):
        """Test __str__ method"""
        conference = Conference.objects.create(**self.conference_data)
        expected_str = f"{conference.name} ({conference.start_date.year})"
        self.assertEqual(str(conference), expected_str)
    
    def test_end_date_before_start_date_validation(self):
        """Test validation: end date phải sau start date"""
        data = self.conference_data.copy()
        data['end_date'] = data['start_date'] - timedelta(days=1)
        
        conference = Conference(**data)
        
        with self.assertRaises(ValidationError):
            conference.clean()
    
    def test_review_deadline_before_submission_validation(self):
        """Test validation: review deadline phải sau submission deadline"""
        data = self.conference_data.copy()
        data['review_deadline'] = data['submission_deadline'] - timedelta(days=1)
        
        conference = Conference(**data)
        
        with self.assertRaises(ValidationError):
            conference.clean()
    
    def test_is_submission_open(self):
        """Test kiểm tra submission có đang mở không"""
        conference = Conference.objects.create(**self.conference_data)
        
        # Draft status - not open
        self.assertFalse(conference.is_submission_open())
        
        # Open status - should be open
        conference.status = 'open'
        conference.save()
        self.assertTrue(conference.is_submission_open())
        
        # Past deadline - not open
        conference.submission_deadline = timezone.now() - timedelta(days=1)
        conference.save()
        self.assertFalse(conference.is_submission_open())
    
    def test_is_past_deadline(self):
        """Test kiểm tra đã qua deadline chưa"""
        conference = Conference.objects.create(**self.conference_data)
        
        # Future deadline
        self.assertFalse(conference.is_past_deadline())
        
        # Past deadline
        conference.submission_deadline = timezone.now() - timedelta(days=1)
        conference.save()
        self.assertTrue(conference.is_past_deadline())
    
    def test_days_until_deadline(self):
        """Test tính số ngày còn lại"""
        conference = Conference.objects.create(**self.conference_data)
        
        days = conference.days_until_deadline()
        self.assertGreater(days, 0)
        
        # Past deadline
        conference.submission_deadline = timezone.now() - timedelta(days=5)
        conference.save()
        self.assertEqual(conference.days_until_deadline(), 0)
    
    def test_open_for_submission(self):
        """Test mở conference cho submission"""
        conference = Conference.objects.create(**self.conference_data)
        
        # Should be in draft status
        self.assertEqual(conference.status, 'draft')
        
        # Open for submission
        conference.open_for_submission()
        
        self.assertEqual(conference.status, 'open')
    
    def test_open_for_submission_from_non_draft_fails(self):
        """Test không thể open submission từ status khác draft"""
        conference = Conference.objects.create(**self.conference_data)
        conference.status = 'review'
        conference.save()
        
        with self.assertRaises(ValidationError):
            conference.open_for_submission()
    
    def test_close_submission(self):
        """Test đóng submission"""
        conference = Conference.objects.create(**self.conference_data)
        conference.status = 'open'
        conference.save()
        
        conference.close_submission()
        
        self.assertEqual(conference.status, 'review')
    
    def test_complete_conference(self):
        """Test hoàn thành conference"""
        conference = Conference.objects.create(**self.conference_data)
        
        conference.complete()
        
        self.assertEqual(conference.status, 'completed')
    
    def test_archive_conference(self):
        """Test archive conference"""
        conference = Conference.objects.create(**self.conference_data)
        
        conference.archive()
        
        self.assertEqual(conference.status, 'archived')


class TrackModelTestCase(TestCase):
    """Test cases cho Track model"""
    
    def setUp(self):
        """Setup test data"""
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
            venue='Test Venue',
            city='Test City',
            country='Test Country',
            chair=chair,
        )
    
    def test_create_track(self):
        """Test tạo track"""
        track = Track.objects.create(
            conference=self.conference,
            name='Machine Learning',
            description='ML track',
            chair=self.conference.chair
        )
        
        self.assertEqual(track.name, 'Machine Learning')
        self.assertEqual(track.conference, self.conference)
        self.assertTrue(track.is_active)
    
    def test_track_str_representation(self):
        """Test __str__ method"""
        track = Track.objects.create(
            conference=self.conference,
            name='Computer Vision'
        )
        
        expected_str = f"{self.conference.acronym} - {track.name}"
        self.assertEqual(str(track), expected_str)
    
    def test_unique_track_per_conference(self):
        """Test track name phải unique trong conference"""
        Track.objects.create(
            conference=self.conference,
            name='AI'
        )
        
        # Tạo track thứ 2 với cùng tên trong cùng conference
        with self.assertRaises(Exception):
            Track.objects.create(
                conference=self.conference,
                name='AI'
            )


class TopicModelTestCase(TestCase):
    """Test cases cho Topic model"""
    
    def test_create_topic(self):
        """Test tạo topic"""
        topic = Topic.objects.create(
            name='Deep Learning',
            description='Neural networks and deep learning'
        )
        
        self.assertEqual(topic.name, 'Deep Learning')
        self.assertTrue(topic.is_active)
    
    def test_topic_unique_constraint(self):
        """Test topic name phải unique"""
        Topic.objects.create(name='Machine Learning')
        
        with self.assertRaises(Exception):
            Topic.objects.create(name='Machine Learning')
    
    def test_hierarchical_topics(self):
        """Test parent-child relationship"""
        parent = Topic.objects.create(name='Artificial Intelligence')
        child = Topic.objects.create(
            name='Machine Learning',
            parent=parent
        )
        
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.subtopics.all())


class PolicySettingModelTestCase(TestCase):
    """Test cases cho PolicySetting model"""
    
    def setUp(self):
        """Setup test data"""
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
            venue='Test Venue',
            city='Test City',
            country='Test Country',
            chair=chair,
        )
    
    def test_create_policy_setting(self):
        """Test tạo policy setting"""
        policy = PolicySetting.objects.create(
            conference=self.conference,
            max_paper_pages=10,
            min_paper_pages=6,
            min_reviews_per_paper=3,
            allowed_file_formats=['pdf', 'docx'],
            max_file_size_mb=15
        )
        
        self.assertEqual(policy.conference, self.conference)
        self.assertEqual(policy.max_paper_pages, 10)
        self.assertTrue(policy.require_anonymous_submission)
    
    def test_min_pages_greater_than_max_validation(self):
        """Test validation: min pages không được lớn hơn max pages"""
        policy = PolicySetting(
            conference=self.conference,
            max_paper_pages=5,
            min_paper_pages=10
        )
        
        with self.assertRaises(ValidationError):
            policy.clean()
    
    def test_default_values(self):
        """Test default values"""
        policy = PolicySetting.objects.create(
            conference=self.conference
        )
        
        self.assertTrue(policy.allow_multiple_submissions)
        self.assertTrue(policy.require_anonymous_submission)
        self.assertEqual(policy.max_paper_pages, 8)
        self.assertEqual(policy.min_paper_pages, 4)
        self.assertEqual(policy.min_reviews_per_paper, 3)


class SystemLogModelTestCase(TestCase):
    """Test cases cho SystemLog"""
    
    def setUp(self):
        """Setup test data"""
        self.user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
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
            venue='Test Venue',
            city='Test City',
            country='Test Country',
            chair=self.user,
        )
    
    def test_create_system_log(self):
        """Test tạo system log"""
        log = SystemLog.objects.create(
            conference=self.conference,
            log_type='conference_created',
            user=self.user,
            description='Conference created',
            ip_address='192.168.1.1',
            metadata={'action': 'create'}
        )
        
        self.assertEqual(log.conference, self.conference)
        self.assertEqual(log.log_type, 'conference_created')
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.ip_address, '192.168.1.1')


# ============================================
# API TESTS
# ============================================

class ConferenceAPITestCase(APITestCase):
    """Test cases cho Conference APIs"""
    
    def setUp(self):
        """Setup test client and data"""
        self.client = APIClient()
        
        # Create chair user
        self.chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='chairpass123',
            full_name='Program Chair',
            status='active'
        )
        
        # Create normal user
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='userpass123',
            status='active'
        )
        
        # Create conference
        self.conference = Conference.objects.create(
            name='International Conference on ML',
            acronym='ICML',
            description='ML Conference',
            start_date=timezone.now().date() + timedelta(days=180),
            end_date=timezone.now().date() + timedelta(days=183),
            submission_deadline=timezone.now() + timedelta(days=90),
            review_deadline=timezone.now() + timedelta(days=120),
            venue='Convention Center',
            city='Vienna',
            country='Austria',
            chair=self.chair,
            status='draft'
        )
        
        self.list_url = reverse('conference-list')
        self.detail_url = reverse('conference-detail', args=[self.conference.conference_id])
    
    def test_list_conferences_unauthenticated(self):
        """Test lấy danh sách conferences không cần authenticate"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_conference_detail(self):
        """Test lấy chi tiết conference"""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.conference.name)
    
    def test_filter_conferences_by_status(self):
        """Test filter conferences theo status"""
        response = self.client.get(self.list_url, {'status': 'draft'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for conf in response.data:
            self.assertEqual(conf['status'], 'draft')
    
    def test_search_conferences(self):
        """Test search conferences"""
        response = self.client.get(self.list_url, {'search': 'ICML'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_get_upcoming_conferences(self):
        """Test lấy upcoming conferences"""
        url = reverse('conference-upcoming')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_open_for_submission_conferences(self):
        """Test lấy conferences đang mở submission"""
        # Set conference to open
        self.conference.status = 'open'
        self.conference.save()
        
        url = reverse('conference-open-for-submission')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_conference_requires_admin(self):
        """Test tạo conference cần quyền admin/chair"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'New Conference',
            'acronym': 'NC',
            'description': 'Test',
            'start_date': (timezone.now().date() + timedelta(days=200)).isoformat(),
            'end_date': (timezone.now().date() + timedelta(days=203)).isoformat(),
            'submission_deadline': (timezone.now() + timedelta(days=100)).isoformat(),
            'review_deadline': (timezone.now() + timedelta(days=130)).isoformat(),
            'venue': 'Test',
            'city': 'Test',
            'country': 'Test',
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        # Should fail because user is not admin/chair
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_open_submission_as_chair(self):
        """Test chair có thể mở submission"""
        self.client.force_authenticate(user=self.chair)
        
        url = reverse('conference-open-submission', args=[self.conference.conference_id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify status changed
        self.conference.refresh_from_db()
        self.assertEqual(self.conference.status, 'open')
    
    def test_close_submission_as_chair(self):
        """Test chair có thể đóng submission"""
        self.conference.status = 'open'
        self.conference.save()
        
        self.client.force_authenticate(user=self.chair)
        
        url = reverse('conference-close-submission', args=[self.conference.conference_id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify status changed
        self.conference.refresh_from_db()
        self.assertEqual(self.conference.status, 'review')
    
    def test_get_conference_statistics(self):
        """Test lấy statistics của conference"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('conference-statistics', args=[self.conference.conference_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_papers', response.data)
        self.assertIn('total_tracks', response.data)
        self.assertIn('days_until_deadline', response.data)
    
    def test_get_conference_tracks(self):
        """Test lấy tracks của conference"""
        # Create track
        Track.objects.create(
            conference=self.conference,
            name='AI Track'
        )
        
        url = reverse('conference-tracks', args=[self.conference.conference_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TrackAPITestCase(APITestCase):
    """Test cases cho Track APIs"""
    
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            status='active'
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
        
        self.track = Track.objects.create(
            conference=self.conference,
            name='Machine Learning'
        )
        
        self.list_url = reverse('track-list')
    
    def test_list_tracks(self):
        """Test lấy danh sách tracks"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_filter_tracks_by_conference(self):
        """Test filter tracks theo conference"""
        response = self.client.get(
            self.list_url,
            {'conference': self.conference.conference_id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for track in response.data:
            self.assertEqual(track['conference'], self.conference.conference_id)


class TopicAPITestCase(APITestCase):
    """Test cases cho Topic APIs"""
    
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        
        self.topic1 = Topic.objects.create(name='Machine Learning')
        self.topic2 = Topic.objects.create(name='Deep Learning')
        
        self.list_url = reverse('topic-list')
    
    def test_list_topics(self):
        """Test lấy danh sách topics"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)
    
    def test_get_popular_topics(self):
        """Test lấy popular topics"""
        url = reverse('topic-popular')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================
# INTEGRATION TESTS
# ============================================

class ConferenceWorkflowTestCase(APITestCase):
    """Test complete conference workflow"""
    
    def test_complete_conference_lifecycle(self):
        """
        Test complete workflow:
        1. Create conference
        2. Add tracks
        3. Open for submission
        4. Close submission
        5. Complete conference
        """
        # Create chair
        chair = User.objects.create_user(
            email='chair@example.com',
            username='chair',
            password='pass123',
            status='active',
            is_staff=True  # Make admin for testing
        )
        
        self.client.force_authenticate(user=chair)
        
        # 1. Create conference
        conference_data = {
            'name': 'Test Workflow Conference',
            'acronym': 'TWC',
            'description': 'Testing workflow',
            'start_date': (timezone.now().date() + timedelta(days=180)).isoformat(),
            'end_date': (timezone.now().date() + timedelta(days=183)).isoformat(),
            'submission_deadline': (timezone.now() + timedelta(days=90)).isoformat(),
            'review_deadline': (timezone.now() + timedelta(days=120)).isoformat(),
            'venue': 'Test Venue',
            'city': 'Test City',
            'country': 'Test Country',
            'chair': chair.id
        }
        
        create_url = reverse('conference-list')
        response = self.client.post(create_url, conference_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        conference_id = response.data['conference_id']
        
        # 2. Add track
        track_url = reverse('track-list')
        track_data = {
            'conference': conference_id,
            'name': 'AI Track'
        }
        response = self.client.post(track_url, track_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 3. Open for submission
        open_url = reverse('conference-open-submission', args=[conference_id])
        response = self.client.post(open_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Close submission
        close_url = reverse('conference-close-submission', args=[conference_id])
        response = self.client.post(close_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify final status
        conference = Conference.objects.get(conference_id=conference_id)
        self.assertEqual(conference.status, 'review')
