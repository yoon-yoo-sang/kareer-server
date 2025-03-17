import datetime
import random

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AuthUser
from jobs.models import Job, JobBookmark


class JobsTest(APITestCase):
    def setUp(self):
        job_count = 5
        self.most_bookmarked_job_count = 0
        self.most_recent_job = None
        self.most_bookmarked_job = None

        self.user = AuthUser.objects.create_user(
            username="test",
            email="yysss61888@gmail.com",
            password="password",
            social_provider="email",
            locale="ko-KR",
        )

        for idx in range(job_count):
            job = Job.objects.create(
                title="Software Engineer",
                description="Software Engineer",
                company_name="Google",
                location="Mountain View, CA",
                requirements="BS in Computer Science",
                salary_range="100000-200000",
                category="full_time",
                industry="internet",
                posted_at=timezone.now(),
                expired_at=timezone.now() + datetime.timedelta(days=30),
                is_hiring=True,
            )

            if idx == job_count - 1:
                self.most_recent_job = job

            rand_int = random.randint(1, 5)

            for idx2 in range(rand_int):
                name = f"test{idx}{idx2}"
                user = AuthUser.objects.create_user(
                    username=name,
                    email=f"{name}@gmail.com",
                    password="password",
                    social_provider="email",
                    locale="ko-KR",
                )
                JobBookmark.objects.create(user_id=user.id, job_id=job.id)

            if rand_int > self.most_bookmarked_job_count:
                self.most_bookmarked_job_count = rand_int
                self.most_bookmarked_job = job

        for _ in range(5):
            Job.objects.create(
                title="title",
                description="description",
                company_name="Google",
                location="Mountain View, CA",
                requirements="BS in Computer Science",
                salary_range="100000-200000",
                category="part_time",
                industry="fintech",
                posted_at=timezone.now(),
                expired_at=timezone.now() + datetime.timedelta(days=30),
                is_hiring=True,
            )

    def test_get_jobs(self):
        job_count = 3
        self.authenticate()

        response = self.client.get(
            f"/jobs/jobs?limit={job_count}&offset=0&order_by=recommended&search=Software",
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), job_count)
        self.assertEqual(response.data["results"][0]["id"], self.most_bookmarked_job.id)

        response = self.client.get(
            f"/jobs/jobs?limit={job_count}&offset=0&order_by=recently&search=Software",
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), job_count)
        self.assertEqual(response.data["results"][0]["id"], self.most_recent_job.id)

        response = self.client.get(f"/jobs/jobs/{self.most_recent_job.id}", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.most_recent_job.id)

    def authenticate(self):
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
