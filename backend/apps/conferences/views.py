from rest_framework import viewsets
from .models import Conference
from .serializers import ConferenceSerializer

class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


