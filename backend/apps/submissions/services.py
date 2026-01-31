from django.utils import timezone
from django.db import transaction
VALID_TRANSITIONS = {
    "submitted": ["under_review"],
    "under_review": ["accepted", "rejected"],
    "accepted": ["camera_ready"],
}
@transaction.atomic
def change_status(submission, new_status):
    current = submission.status
    if new_status not in VALID_TRANSITIONS.get(current, []):
        raise ValueError(f"Invalid status transition: {current} -> {new_status}")
    submission.status = new_status
    if new_status == "accepted" and not submission.paper_id:
        year = timezone.now().year
        count = submission.__class__.objects.filter(
            paper_id__startwith=f"UTH-{year}"
        ).count() + 1
        submission.paper_id = f"UTH-{timezone.now().year} - {count:04d}"
    submission.save()
    return submission
def validate_camera_ready(submission):
    if not submission.camera_ready_deadline:
        raise ValueError("Camera ready deadline not set")
    if timezone.now() > submission.camera_ready_deadline:
        raise ValueError("Camera ready deadline passed")