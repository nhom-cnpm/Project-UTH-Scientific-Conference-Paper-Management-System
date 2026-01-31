from fastapi import APIRouter, HTTPException
from apps.submissions.models import Submission
from apps.submissions.services import change_status
router = APIRouter(prefix="/submissions", tags=["Submissions"])
@router.post("/{submission_id}/decision")
def decision_submission(submission_id: int, decision: str):
    if decision not in ["accept", "reject"]:
        raise HTTPExeption(400, "Decision must be accept or reject")
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
        raise HTTPException(404, "Submission not found")
    except ValueError as e:
        raise HTTPException(400, str(e))
    
# @router.get("/{submission_id}/status")
# def submission_status(submission_id: int):
#     submission = Submission.objects.filter(id=submission_id)
#     return{
#         "status": submission.status,
#         "paper_id": submission.paper_id
#     }