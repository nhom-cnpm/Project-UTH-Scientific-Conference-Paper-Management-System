from fastapi import APIRouter
from apps.submissions.models import Submission
router = APIRouter(prefix ="/program",  tags=["Program"])
@router.get("/{conference_id}")
def program_list(conference_id: int):
    papers = Submission.objects.filter(status="accepted")
    return [{
        "paper_id": p.paper_id,
        "title": p.title
    }
    for p in papers]
@router.get("/{conference_id}/export")
def export_program(conference_id: int):
    papers = Submission.objects.filter(status="accepted")
    return{
        "conference_id": conference_id,
        "papers": [{
            "paper_id": p.paper_id,
            "title": p.title
        }
        for p in papers]
    }