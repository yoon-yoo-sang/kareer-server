from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import AuthUser


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.social_user = AuthUser.objects.create_user(
            username='google_123456',
            social_id='123456',
            social_provider='google',
            email='asdf1234@gmail.com',
            locale='ko',
        )

        self.email_user = AuthUser.objects.create_user(
            username='yys618@naver.com',
            email='yys618@naver.com',
            password='password',
            social_provider='email',
            locale='ko-KR',
        )

    def test_social_sign_up_success(self):
        url = reverse('auth:sign-up')
        data = {
            'social_id': '1234567890',
            'social_provider': 'google',
            'email': 'qazwsx123@gmail.com',
            'locale': 'ko'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

        user = AuthUser.objects.get(social_id='1234567890')
        self.assertEqual(user.social_provider, 'google')
        self.assertEqual(user.locale, 'ko')


    def test_email_sign_up_success(self):
        url = reverse('auth:sign-up')
        data = {
            'email': 'yysss61888@gmail.com',
            'password': 'password',
            'locale': 'ko-KR',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

        user = AuthUser.objects.get(email='yysss61888@gmail.com')
        self.assertEqual(user.locale, 'ko-KR')
        self.assertEqual(user.social_provider, 'email')

    def test_social_sign_in_success(self):
        url = reverse('auth:sign-in')
        data = {
            'social_id': '123456',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_email_sign_in_success(self):
        url = reverse('auth:sign-in')
        data = {
            'email': 'yys618@naver.com',
            'password': 'password',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
