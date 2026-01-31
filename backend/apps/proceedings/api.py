from fastapi import APIRouter
from apps.submissions.models import Submission
router = APIRouter(prefix ="/program",  tags=["Program"])
@router.get("/{conference_id}")
def program_list(conference_id: int):
    papers = Submission.objects.filter(status="accepted").values("paper_id", "title")
    return list(papers)

@router.get("/{conference_id}/export")
def export_program(conference_id: int):
    papers = Submission.objects.filter(status="accepted").values("paper_id", "title")
    return{
        "conference_id": conference_id,
        "total": papers.count(),
        "papers": list(papers)
    }