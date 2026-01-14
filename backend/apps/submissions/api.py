from fastapi import APIRouter, HTTPException
from apps.submissions.models import Submission
from apps.submissions.services import make_decision
router = APIRouter(prefix="/submissions", tags=["Submissions"])
@router.post("/{submission_id}/decision")
def decision_submission(submission_id: int, decision: str):
    try:
        submission = Submission.objects.get(id=submission_id)
        submission = make_decision(submission, decision)
        return {
            "id": submission.id,
            "status": submission.status,
            "paper_code": submission.paper_code
        }
    except Submission.DoesNotExist:
        raise HTTPException(status_code=404, detail="Submission not found")