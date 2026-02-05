from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.submissions.models import Submission

BASE_URL = "/api/submissions"
class BE4DecisionCameraReadyProgramTest(TestCase):
    """
    Test cho BE4:
    - Decision (Accept / Reject)
    - Camera-ready
    - Program
    """

    def setUp(self):
        self.client = Client()

        self.submission = Submission.objects.create(
            title="AI in Healthcare",
            status="submitted"
        )

        self.accepted_submission = Submission.objects.create(
            title="Blockchain Research",
            status="accepted",
            paper_id="PAPER-001"
        )


    def test_accept_submission(self):
        """
        API Accept submission
        """
        url = f"{BASE_URL}/{self.submission.id}/decision/?decision=accept"
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, "accepted")
        self.assertIsNotNone(self.submission.paper_id)

    def test_reject_submission(self):
        """
        API Reject submission
        """
        submission = Submission.objects.create(
            title="Rejected paper",
            status="submitted"
        )

        url = f"{BASE_URL}/{submission.id}/decision/?decision=reject"
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        submission.refresh_from_db()
        self.assertEqual(submission.status, "rejected")

    def test_display_submission_status(self):
        """
        API display status
        """
        self.assertEqual(self.submission.status, "submitted")

    def test_list_accepted_submissions(self):
        """
        Lấy danh sách accepted submissions
        """
        response = self.client.get("/submission/accepted/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["paper_id"], "PAPER-001")

    def test_status_transition_logic(self):
        """
        submitted → accepted
        """
        self.submission.status = "submitted"
        self.submission.save()

        url = f"{BASE_URL}/{self.submission.id}/decision/?decision=accept"
        self.client.post(url)

        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, "accepted")

    def test_program_list_api(self):
        """
        API program: list accepted papers
        """
        response = self.client.get("/submission/program/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("program", response.json())
        self.assertEqual(len(response.json()["program"]), 1)



    def test_export_program_json(self):
        """
        Xuất program JSON
        """
        response = self.client.get("/submission/program/")

        data = response.json()
        self.assertIn("program", data)
        self.assertEqual(data["program"][0]["paper_id"], "PAPER-001")

    def test_camera_ready_upload_success(self):
        """
        Upload camera-ready hợp lệ
        """
        submission = Submission.objects.create(
            title="Camera Ready Paper",
            status="accepted",
            camera_ready_deadline=timezone.now() + timezone.timedelta(days=1)
        )

        file = SimpleUploadedFile(
            "paper.pdf",
            b"dummy pdf content",
            content_type="application/pdf"
        )

        url = f"{BASE_URL}/{submission.id}/camera-ready/"
        response = self.client.post(url, {"file": file})

        self.assertEqual(response.status_code, 200)

        submission.refresh_from_db()
        self.assertEqual(submission.status, "camera_ready")

    def test_camera_ready_deadline_invalid(self):
        """
        Validate camera-ready deadline (quá hạn)
        """
        submission = Submission.objects.create(
            title="Late Paper",
            status="accepted",
            camera_ready_deadline=timezone.now() - timezone.timedelta(days=1)
        )

        file = SimpleUploadedFile(
            "paper.pdf",
            b"late file",
            content_type="application/pdf"
        )

        url = f"{BASE_URL}/{submission.id}/camera-ready/"
        response = self.client.post(url, {"file": file})

        self.assertEqual(response.status_code, 400)
