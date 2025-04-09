from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model  # وارد کردن مدل کاربر سفارشی
from rest_framework import status
from django.urls import reverse
from .models import Review, SentimentAnalysis

'''class IntegrationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # استفاده از مدل کاربر سفارشی
        User = get_user_model()

        # ساخت یک کاربر عادی و یک کاربر ادمین
        self.user = User.objects.create_user(username="user", password="password123")
        self.admin = User.objects.create_superuser(username="admin", password="admin123")

        # دریافت توکن JWT برای هر دو
        login_url = reverse('token_obtain_pair')
        self.user_token = self.client.post(login_url, {"username": "user", "password": "password123"}).data['access']
        self.admin_token = self.client.post(login_url, {"username": "admin", "password": "admin123"}).data['access']

        self.review_url = reverse('review-list')  # فرض: endpoint ایجاد و دیدن نظرات

    def test_login_success_and_failure(self):
        """1) تست لاگین موفق و ناموفق"""
        url = reverse('token_obtain_pair')

        # لاگین موفق
        response = self.client.post(url, {"username": "user", "password": "password123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

        # لاگین ناموفق
        response = self.client.post(url, {"username": "user", "password": "wrongpass"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("No active account", str(response.data))

    def test_user_role_permission(self):
        """2) فقط ادمین می‌تواند کامنت حذف کند"""
        # ایجاد یک review توسط یوزر
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(self.review_url, {"review_text": "Test review"}, format='json')
        review_id = response.data['id']

        # تلاش برای حذف review توسط یوزر عادی
        response = self.client.delete(reverse('review-detail', args=[review_id]))
        self.assertEqual(response.status_code, 403)

        # تلاش برای حذف review توسط ادمین
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(reverse('review-detail', args=[review_id]))
        self.assertEqual(response.status_code, 204)

    def test_unauthorized_access(self):
        """3) تست دسترسی بدون توکن"""
        # بدون توکن: ارسال review
        response = self.client.post(self.review_url, {"review_text": "Unauthorized"}, format='json')
        self.assertEqual(response.status_code, 401)

        # بدون توکن: گرفتن لیست reviewها
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, 401)

    def test_sentiment_analysis_on_review_creation(self):
        """4) بررسی تحلیل احساسات پس از ایجاد review"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(self.review_url, {"review_text": "This is a great product!"}, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        # بررسی اینکه تحلیل احساسات به درستی ذخیره شده باشد
        review_id = response.data['id']
        sentiment_analysis = SentimentAnalysis.objects.get(review_id=review_id)
        self.assertIn(sentiment_analysis.sentiment, ['positive', 'negative'])
        self.assertGreater(sentiment_analysis.confidence, 0.5)

       def test_ajax_request(self):
        """5) ارسال درخواست AJAX برای ایجاد review"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(
            self.review_url,
            {"review_text": "Review from AJAX"},
            format='json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['review_text'], "Review from AJAX")


class IntegrationTests(APITestCase):
    def setUp(self):
        self.review_url = '/api/submit-comment/'  # Correct endpoint

    def test_unauthorized_access(self):
        response = self.client.post(self.review_url, {"review_text": "Unauthorized"}, format='json')
        self.assertEqual(response.status_code, 401)  # Assuming 401 for unauthorized access'''



def test_login_success_and_failure(self):
        """1) تست لاگین موفق و ناموفق"""
        url = reverse('token_obtain_pair')

        # لاگین موفق
        response = self.client.post(url, {"username": "user", "password": "password123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
