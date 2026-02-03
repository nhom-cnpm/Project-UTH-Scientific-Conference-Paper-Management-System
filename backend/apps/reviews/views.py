
from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer

class ReviewerViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import ReviewAssignment, Review
from .serializers import AssignReviewerSerializer, ReviewSerializer
class AssignReviewerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssignReviewerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assignment = serializer.save(
            assigned_by=request.user, status="assigned"
        )

        return Response(
            {"message": "Reviewer assigned successfully", "id": assignment.id},
            status=status.HTTP_201_CREATED,
        )
class MyAssignedPapersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assignments = ReviewAssignment.objects.filter(
            reviewer=request.user
        ).select_related("paper")

        data = [
            {
                "assignment_id": a.id,
                "paper_id": a.paper.id,
                "paper_title": getattr(a.paper, "title", ""),
                "status": a.status,
            }
            for a in assignments
        ]

        return Response(data)
class SubmitReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        review = serializer.save()
        review.assignment.status = "completed"
        review.assignment.save()

        return Response(
            {"message": "Review submitted successfully", "review_id": review.id},
            status=status.HTTP_201_CREATED,
        )
