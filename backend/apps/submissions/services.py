from django.utils import timezone
def change_status(submission, new_status):
    """
    Kiểm soát luồng trạng thái bài nộp.
    """
    allowed = {
        "submitted": ["under_review"],
        "under_review": ["accepted", "rejected"],
        "accepted": ["camera_ready"],
    }
    if new_status not in allowed.get(submission.status, []):
        raise ValueError("Invalid status transition")
    submission.status = new_status
    if new_status == "accepted":
        submission.paper_id = f"UTH-{submission.id}"
    submission.save()
    return submission
def validate_camera_ready(submission):
    """
    Check dealine camera ready
    """
    if timezone.now() > submission.camera_ready_deadline:
        raise ValueError("Camera ready deadline passed")