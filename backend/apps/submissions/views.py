from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.submissions.models import Submission, Topic
from apps.submissions.services import change_status, validate_camera_ready
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SubmissionSerializer

# Create your views here.
@require_http_methods(["POST"])
def decision_submission(request, submission_id):
    decision = request.GET.get("decision")

    try:
        submission = Submission.objects.get(id=submission_id)
        new_status = "accepted" if decision == "accept" else "rejected"
        submission = change_status(submission, new_status)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "id": submission.id,
        "status": submission.status,
        "paper_id": submission.paper_id,
    })
def accepted_list(request):
    qs=Submission.objects.filter(status="accepted")
    data=list(qs.values("id","title", "paper_id"))
    return JsonResponse(data, safe=False)
def program_json(request):
    """
    Xuat program JSON
    """
    qs = Submission.objects.filter(status="accepted")
    data=list(qs.values("paper_id", "title"))
    return JsonResponse({"program": data})
@require_http_methods(["POST"])
def upload_camera_ready(request, submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        validate_camera_ready(submission)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    submission.camera_ready_file = request.FILES["file"]
    submission.status="camera_ready"
    submission.save()

    return JsonResponse({"message": "Camera-ready uploaded"})
@api_view(["GET"])
def accepted_submisisons(request):
    submissions = Submission.objects.filter(status="accepted")
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)
@api_view(["GET"])
def topics_list(request):
    topics = Topic.objects.all()
    data = [{"id": topic.id, "name": topic.name} for topic in topics]
    return Response(data)