from fastapi import APIRouter, HTTPException
from apps.submissions.models import Submission
from apps.submissions.services import make_decision
router = APIRouter(prefix="/submissions", tags=["Submissions"])
@router.post("/{submission_id}/decision")
def decision_submission(submission_id: int, decision: str):
    """
    Accept / Reject submission
    """
    try:
        submission = Submission.objects.get(id=submission_id)
        submission = make_decision(submission, decision)
        if decision == "accept":
            change_status(submission, "accepted")
        elif decision == "reject":
            change_status(submission, "rejected")
        else:
            raise HTTPException(400, "Invalid decision")
        return {
            "id": submission.id,
            "status": submission.status,
            "paper_code": submission.paper_code
        }
    except Submission.DoesNotExist:
        raise HTTPException(404, "Submission not found")