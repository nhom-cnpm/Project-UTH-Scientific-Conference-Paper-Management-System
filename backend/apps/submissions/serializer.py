from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    # topic = serializers.CharField(source="topic.name", read_only = True)
    class Meta:
        model = Submission
        fields = ["id", "title", "topic", "status"]