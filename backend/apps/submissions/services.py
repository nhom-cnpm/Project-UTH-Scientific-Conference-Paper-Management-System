from django.utils import timezone
from django.db import transaction
import uuid
VALID_TRANSITIONS = {
    "submitted": ["accepted", "rejected","under_review"],
    "under_review": ["accepted", "rejected"],
    "accepted": ["camera_ready"],
}
def generate_paper_id():
    """
    Sinh mã bài nộp: UTH-XXXXX
    """
    return f"UTH-{uuid.uuid4().hex[:6].upper()}"
@transaction.atomic
def change_status(submission, new_status):
    current = submission.status
    if new_status not in VALID_TRANSITIONS.get(current, []):
        raise ValueError(f"Invalid status transition: {current} -> {new_status}")
    submission.status = new_status
    if new_status == "accepted" and not submission.paper_id:
        submission.paper_id = generate_paper_id()
    submission.save()
    return submission
def validate_camera_ready(submission):
    if not submission.camera_ready_deadline:
        raise ValueError("Camera ready deadline not set")
    if timezone.now() > submission.camera_ready_deadline:
        raise ValueError("Camera ready deadline passed")
    if submission.status != "accepted":
        raise ValueError("Submission not accepted")
    return True