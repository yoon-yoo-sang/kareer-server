import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AuthUser
from users.models import UserProfile, UserCareerExperience, UserEducation


class UsersTest(APITestCase):
    def setUp(self):
        self.user = AuthUser.objects.create_user(
            username='google_123456',
            social_id='123456',
            social_provider='google',
            email='yysss61888@gmail.com',
            locale='ko-KR',
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            full_name='윤유상',
            nickname='밥',
            nationality='South Korea',
            occupation='developer',
            skills=['python', 'django'],
            resume_uri='https://resume.com'
        )

        self.career_experiences = [
            UserCareerExperience.objects.create(
                user=self.user,
                company_name='company1',
                job_title='developer',
                started_at=datetime.date(2020, 1, 1),
                ended_at=datetime.date(2021, 1, 1),
                description='description1',
                is_current=False
            ),
            UserCareerExperience.objects.create(
                user=self.user,
                company_name='company2',
                job_title='developer',
                started_at=datetime.date(2021, 1, 1),
                ended_at=None,
                description='description2',
                is_current=True
            )
        ]

        self.educations = [
            UserEducation.objects.create(
                user=self.user,
                school_name='school1',
                major='major1',
                degree='bachelor',
                started_at=datetime.date(2010, 1, 1),
                ended_at=datetime.date(2014, 1, 1),
                description='description1',
                is_current=False
            ),
            UserEducation.objects.create(
                user=self.user,
                school_name='school2',
                major='major2',
                degree='master',
                started_at=datetime.date(2014, 1, 1),
                ended_at=None,
                description='description2',
                is_current=True
            )
        ]

    def authenticate(self):
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    def test_get_and_patch_user_success(self):
        url = reverse('users:me')
        self.authenticate()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'yysss61888@gmail.com')

        response = self.client.patch(url, {'locale': 'en-US'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['locale'], 'en-US')

    def test_get_user_fail(self):
        url = reverse('users:me')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_patch_user_fail(self):
        url = reverse('users:me')

        response = self.client.patch(url, {'locale': 'en-US'})
        self.assertEqual(response.status_code, 401)

    def test_post_get_and_patch_user_setting_success(self):
        url = reverse('users:me-setting')
        self.authenticate()

        response = self.client.post(url, {
            'is_email_notification_enabled': False,
            'is_push_notification_enabled': False,
            'language': 'en'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_email_notification_enabled'], False)
        self.assertEqual(response.data['is_push_notification_enabled'], False)
        self.assertEqual(response.data['language'], 'en')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_email_notification_enabled'], False)
        self.assertEqual(response.data['is_push_notification_enabled'], False)
        self.assertEqual(response.data['language'], 'en')

        response = self.client.patch(url, {
            'is_email_notification_enabled': True,
            'is_push_notification_enabled': True,
            'language': 'ko'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_email_notification_enabled'], True)
        self.assertEqual(response.data['is_push_notification_enabled'], True)
        self.assertEqual(response.data['language'], 'ko')

    def test_post_user_setting_fail(self):
        url = reverse('users:me-setting')

        response = self.client.post(url, {
            'is_email_notification_enabled': False,
            'is_push_notification_enabled': False,
            'language': 'en'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_success(self):
        url = reverse('users:me-profile')
        self.authenticate()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], '윤유상')

        response = self.client.patch(url, {'full_name': '윤유상2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], '윤유상2')

    def test_user_profile_fail(self):
        url = reverse('users:me-profile')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(url, {'full_name': '윤유상2'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_whole_career_success(self):
        url = reverse('users:me-whole-career')
        self.authenticate()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['full_name'], '윤유상')
        self.assertEqual(len(response.data['career_experiences']), 2)
        self.assertEqual(len(response.data['educations']), 2)

        response = self.client.patch(
            url,
            data = {
                'profile': {
                    'full_name': '윤유상2',
                    'nickname': '밥2',
                },
                'career_experiences': [
                    {
                        'company_name': 'company3',
                        'job_title': 'developer',
                        'started_at': '2021-01-01',
                        'ended_at': None,
                        'description': 'description3',
                        'is_current': True
                    }
                ],
                'educations': [
                    {
                        'school_name': 'school3',
                        'major': 'major3',
                        'degree': 'bachelor',
                        'started_at': '2015-01-01',
                        'ended_at': None,
                        'description': 'description3',
                        'is_current': True
                    }
                ]
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['full_name'], '윤유상2')
        self.assertEqual(response.data['profile']['nickname'], '밥2')
        self.assertEqual(len(response.data['career_experiences']), 1)
        self.assertEqual(len(response.data['educations']), 1)

    def test_whole_career_fail(self):
        url = reverse('users:me-whole-career')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(url, {
            'full_name': '윤유상',
            'nickname': '밥',
            'career_experiences': [
                {
                    'company_name': 'company_failed',
                    'job_title': 'developer',
                    'started_at': '2021-01-01',
                    'ended_at': None,
                    'description': 'description3',
                    'is_current': True
                }
            ],
            'educations': [
                {
                    'school_name': 'school_failed',
                    'major': 'major',
                    'degree': 'bachelor',
                    'started_at': '2015-01-01',
                    'ended_at': None,
                    'description': 'description3',
                    'is_current': True
                }
            ]
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def authenticate(self):
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
