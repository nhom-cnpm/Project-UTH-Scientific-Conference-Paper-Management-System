from fastapi import APIRouter, HTTPException
from apps.submissions.models import Submission
from apps.submissions.services import change_status
router = APIRouter(prefix="/submissions", tags=["Decision"])
@router.post("/{submission_id}/decision")
def decision_submission(submission_id: int, decision: str):
    if decision not in ["accept", "reject"]:
        raise HTTPException(400, "Decision must be accept or reject")
    try:
        submission = Submission.objects.get(id=submission_id)
        new_status = "accepted" if decision == "accept" else "rejected"
        change_status(submission, new_status)
        return {
            "id": submission.id,
            "status": submission.status,
            "paper_code": submission.paper_id
        }
    except Submission.DoesNotExist:
        raise HTTPException(404, detail="Submission not found")
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    
