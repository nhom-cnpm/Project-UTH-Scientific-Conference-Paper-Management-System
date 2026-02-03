from rest_framework import serializers
from .models import Review
from .models import ReviewAssignment, Review


class AssignReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAssignment
        fields = ["paper", "reviewer"]

    def validate(self, data):
        
        if ReviewAssignment.objects.filter(
            paper=data["paper"], reviewer=data["reviewer"]
        ).exists():
            raise serializers.ValidationError("Reviewer already assigned to this paper.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        fields = ["assignment", "score", "comment"]

    def validate_assignment(self, assignment):
        request = self.context["request"]

        
        if assignment.reviewer != request.user:
            raise serializers.ValidationError("You are not assigned to review this paper.")

        
        if hasattr(assignment, "review"):
            raise serializers.ValidationError("Review already submitted for this assignment.")

        return assignment
