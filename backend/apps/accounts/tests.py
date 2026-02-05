from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from .models import Role, UserConferenceRole, UserNotificationPreference

User = get_user_model()

# Create your tests here.
# ============================================
# MODEL TESTS
# ============================================

class UserModelTestCase(TestCase):
    """Test cases cho User model"""
    
    def setUp(self):
        """Setup test data"""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'full_name': 'Test User',
            'affiliation': 'Test University'
        }
    
    def test_create_user(self):
        """Test tạo user thành công"""
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password'],
            full_name=self.user_data['full_name']
        )
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.full_name, self.user_data['full_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.status, 'pending')
        self.assertFalse(user.email_verified)
    
    def test_user_str_representation(self):
        """Test __str__ method"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123',
            full_name='John Doe'
        )
        
        self.assertEqual(str(user), 'John Doe (test@example.com)')
    
    def test_user_without_full_name(self):
        """Test user không có full_name"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        
        self.assertEqual(str(user), 'testuser (test@example.com)')
    
    def test_auto_generate_username(self):
        """Test tự động tạo username từ email"""
        user = User.objects.create_user(
            email='john.doe@example.com',
            password='pass123'
        )
        
        # Username được tạo từ phần trước @ của email
        self.assertTrue(user.username)
        self.assertIn('john.doe', user.username)
    
    def test_email_unique_constraint(self):
        """Test email phải unique"""
        User.objects.create_user(
            email='test@example.com',
            username='user1',
            password='pass123'
        )
        
        # Tạo user thứ 2 với cùng email
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',
                username='user2',
                password='pass123'
            )
    
    def test_activate_user(self):
        """Test activate user"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123',
            status='pending'
        )
        
        user.activate()
        
        self.assertEqual(user.status, 'active')
        self.assertTrue(user.email_verified)
    
    def test_deactivate_user(self):
        """Test deactivate user"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123',
            status='active'
        )
        
        user.deactivate()
        
        self.assertEqual(user.status, 'inactive')
        self.assertFalse(user.is_active)
    
    def test_update_last_login(self):
        """Test update last login"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        
        self.assertIsNone(user.last_login_at)
        
        user.update_last_login()
        
        self.assertIsNotNone(user.last_login_at)


class RoleModelTestCase(TestCase):
    """Test cases cho Role model"""
    
    def test_create_role(self):
        """Test tạo role"""
        role = Role.objects.create(
            name='reviewer',
            display_name='Reviewer',
            description='Paper reviewer'
        )
        
        self.assertEqual(role.name, 'reviewer')
        self.assertEqual(role.display_name, 'Reviewer')
        self.assertEqual(str(role), 'Reviewer')
    
    def test_role_unique_constraint(self):
        """Test role name phải unique"""
        Role.objects.create(
            name='reviewer',
            display_name='Reviewer'
        )
        
        with self.assertRaises(Exception):
            Role.objects.create(
                name='reviewer',
                display_name='Reviewer 2'
            )


class UserConferenceRoleTestCase(TestCase):
    """Test cases cho UserConferenceRole"""
    
    def setUp(self):
        """Setup test data"""
        self.user = User.objects.create_user(
            email='reviewer@example.com',
            username='reviewer',
            password='pass123'
        )
        
        self.role = Role.objects.create(
            name='reviewer',
            display_name='Reviewer'
        )
        
        # Note: Conference model cần được tạo hoặc mock
        # Giả sử có Conference model
        # from conferences.models import Conference
        # self.conference = Conference.objects.create(name='Test Conference')
    
    def test_create_user_conference_role(self):
        """Test tạo user conference role"""
        # Skip nếu chưa có Conference model
        self.skipTest("Requires Conference model")
    
    def test_is_expired(self):
        """Test kiểm tra role expired"""
        # Skip nếu chưa có Conference model
        self.skipTest("Requires Conference model")


class UserNotificationPreferenceTestCase(TestCase):
    """Test cases cho UserNotificationPreference"""
    
    def test_create_notification_preference(self):
        """Test tạo notification preference"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        
        pref = UserNotificationPreference.objects.create(user=user)
        
        # Check default values
        self.assertTrue(pref.email_on_paper_submitted)
        self.assertTrue(pref.email_on_review_assigned)
        self.assertTrue(pref.in_app_notifications)
        self.assertFalse(pref.daily_digest)
    
    def test_update_notification_preference(self):
        """Test update notification preference"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        
        pref = UserNotificationPreference.objects.create(user=user)
        
        pref.email_on_paper_submitted = False
        pref.daily_digest = True
        pref.save()
        
        # Reload from DB
        pref.refresh_from_db()
        
        self.assertFalse(pref.email_on_paper_submitted)
        self.assertTrue(pref.daily_digest)


# ============================================
# API TESTS
# ============================================

class AuthenticationAPITestCase(APITestCase):
    """Test cases cho Authentication APIs"""
    
    def setUp(self):
        """Setup test client and data"""
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
            'full_name': 'Test User',
            'affiliation': 'Test University'
        }
    
    def test_user_registration_success(self):
        """Test đăng ký user thành công"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user_id', response.data)
        
        # Verify user được tạo trong DB
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        
        # Verify notification preferences được tạo
        user = User.objects.get(email=self.user_data['email'])
        self.assertTrue(hasattr(user, 'notification_preferences'))
    
    def test_user_registration_password_mismatch(self):
        """Test đăng ký với password không khớp"""
        data = self.user_data.copy()
        data['password_confirm'] = 'DifferentPass123!'
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_user_registration_duplicate_email(self):
        """Test đăng ký với email đã tồn tại"""
        # Tạo user đầu tiên
        User.objects.create_user(
            email='test@example.com',
            username='existinguser',
            password='pass123'
        )
        
        # Thử đăng ký với cùng email
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_missing_fields(self):
        """Test đăng ký thiếu trường bắt buộc"""
        data = {
            'email': 'test@example.com'
            # Thiếu username, password
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
    
    def test_user_login_success(self):
        """Test login thành công"""
        # Tạo active user
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            status='active'
        )
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
        # Verify last_login_at được update
        user.refresh_from_db()
        self.assertIsNotNone(user.last_login_at)
    
    def test_user_login_wrong_password(self):
        """Test login với password sai"""
        User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='correctpass123',
            status='active'
        )
        
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpass123'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_user_login_inactive_account(self):
        """Test login với account inactive"""
        User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            status='inactive'
        )
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_user_login_pending_account(self):
        """Test login với account pending"""
        User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            status='pending'
        )
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAPITestCase(APITestCase):
    """Test cases cho User APIs"""
    
    def setUp(self):
        """Setup authenticated user"""
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            full_name='Test User',
            status='active'
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_get_current_user(self):
        """Test lấy thông tin user hiện tại"""
        url = reverse('user-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['full_name'], self.user.full_name)
    
    def test_update_profile(self):
        """Test update profile"""
        url = reverse('user-update-profile')
        data = {
            'full_name': 'Updated Name',
            'affiliation': 'New University',
            'bio': 'This is my bio'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify changes
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, 'Updated Name')
        self.assertEqual(self.user.affiliation, 'New University')
        self.assertEqual(self.user.bio, 'This is my bio')
    
    def test_change_password_success(self):
        """Test đổi password thành công"""
        url = reverse('user-change-password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewStrongPass123!',
            'new_password_confirm': 'NewStrongPass123!'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewStrongPass123!'))
    
    def test_change_password_wrong_old_password(self):
        """Test đổi password với old password sai"""
        url = reverse('user-change-password')
        data = {
            'old_password': 'wrongpass',
            'new_password': 'NewStrongPass123!',
            'new_password_confirm': 'NewStrongPass123!'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_change_password_mismatch(self):
        """Test đổi password với confirm không khớp"""
        url = reverse('user-change-password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewStrongPass123!',
            'new_password_confirm': 'DifferentPass123!'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_unauthenticated_access(self):
        """Test truy cập khi chưa authenticate"""
        self.client.force_authenticate(user=None)
        
        url = reverse('user-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RoleAPITestCase(APITestCase):
    """Test cases cho Role APIs"""
    
    def setUp(self):
        """Setup authenticated user and roles"""
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            status='active'
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create roles
        self.role1 = Role.objects.create(
            name='author',
            display_name='Author'
        )
        self.role2 = Role.objects.create(
            name='reviewer',
            display_name='Reviewer'
        )
    
    def test_list_roles(self):
        """Test lấy danh sách roles"""
        url = reverse('role-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_role_detail(self):
        """Test lấy chi tiết role"""
        url = reverse('role-detail', args=[self.role1.role_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'author')
        self.assertEqual(response.data['display_name'], 'Author')


# ============================================
# INTEGRATION TESTS
# ============================================

class UserWorkflowTestCase(APITestCase):
    """Test full user workflow"""
    
    def test_complete_user_workflow(self):
        """
        Test complete workflow:
        1. Register
        2. Login
        3. Update profile
        4. Change password
        """
        # 1. Register
        register_data = {
            'email': 'workflow@example.com',
            'username': 'workflowuser',
            'password': 'InitialPass123!',
            'password_confirm': 'InitialPass123!',
            'full_name': 'Workflow User'
        }
        
        register_url = reverse('register')
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Activate user manually (in real app, this would be via email)
        user = User.objects.get(email='workflow@example.com')
        user.activate()
        
        # 2. Login
        login_data = {
            'email': 'workflow@example.com',
            'password': 'InitialPass123!'
        }
        
        login_url = reverse('login')
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Authenticate for subsequent requests
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # 3. Update profile
        profile_url = reverse('user-update-profile')
        profile_data = {
            'full_name': 'Updated Workflow User',
            'affiliation': 'Test University'
        }
        
        response = self.client.patch(profile_url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Change password
        password_url = reverse('user-change-password')
        password_data = {
            'old_password': 'InitialPass123!',
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }
        
        response = self.client.post(password_url, password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify can login with new password
        new_login_data = {
            'email': 'workflow@example.com',
            'password': 'NewSecurePass123!'
        }
        
        response = self.client.post(login_url, new_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================
# PERFORMANCE TESTS
# ============================================

class PerformanceTestCase(TestCase):
    """Test performance với large dataset"""
    
    def test_create_many_users(self):
        """Test tạo nhiều users"""
        users = []
        for i in range(100):
            users.append(User(
                email=f'user{i}@example.com',
                username=f'user{i}',
                full_name=f'User {i}'
            ))
        
        # Bulk create
        User.objects.bulk_create(users)
        
        self.assertEqual(User.objects.count(), 100)
    
    def test_query_optimization(self):
        """Test query optimization với select_related"""
        # Create test data
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        
        role = Role.objects.create(
            name='reviewer',
            display_name='Reviewer'
        )
        
        # This would need Conference model
        # conference_role = UserConferenceRole.objects.create(...)
        
        # Test query count
        # with self.assertNumQueries(1):
        #     roles = UserConferenceRole.objects.select_related('user', 'role').all()
        