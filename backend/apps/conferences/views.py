from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db.models import Q, Count

from .models import Conference, Track, Topic, PolicySetting, SystemLog
from .serializers import (
    ConferenceSerializer, ConferenceDetailSerializer,
    TrackSerializer, TopicSerializer, PolicySettingSerializer
)
from accounts.permissions import IsChairOrAdmin

# Create your views here.
class ConferenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Conference
    """
    queryset = Conference.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return ConferenceDetailSerializer
        return ConferenceSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsChairOrAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Conference.objects.filter(is_deleted=False)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by year
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(start_date__year=year)
        
        # Search by name
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(acronym__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.select_related('chair').order_by('-start_date')
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Lấy danh sách conferences sắp diễn ra"""
        now = timezone.now()
        conferences = Conference.objects.filter(
            is_deleted=False,
            start_date__gte=now.date(),
            status__in=['open', 'review']
        ).order_by('start_date')[:10]
        
        serializer = ConferenceSerializer(conferences, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def open_for_submission(self, request):
        """Lấy conferences đang mở submission"""
        conferences = Conference.objects.filter(
            is_deleted=False,
            status='open',
            submission_deadline__gte=timezone.now()
        ).order_by('submission_deadline')
        
        serializer = ConferenceSerializer(conferences, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsChairOrAdmin])
    def open_submission(self, request, pk=None):
        """Mở conference cho submission"""
        conference = self.get_object()
        
        try:
            conference.open_for_submission()
            
            # Log activity
            SystemLog.objects.create(
                conference=conference,
                log_type='submission_opened',
                user=request.user,
                description=f"Submission opened by {request.user.email}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return Response({
                'status': 'success',
                'message': 'Conference opened for submission'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsChairOrAdmin])
    def close_submission(self, request, pk=None):
        """Đóng submission"""
        conference = self.get_object()
        
        try:
            conference.close_submission()
            
            # Log activity
            SystemLog.objects.create(
                conference=conference,
                log_type='submission_closed',
                user=request.user,
                description=f"Submission closed by {request.user.email}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return Response({
                'status': 'success',
                'message': 'Submission closed, moved to review phase'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Lấy thống kê của conference"""
        conference = self.get_object()
        
        stats = {
            'total_papers': conference.papers.count() if hasattr(conference, 'papers') else 0,
            'total_tracks': conference.tracks.count(),
            'total_reviewers': conference.user_roles.filter(
                role__name='reviewer',
                is_active=True
            ).count(),
            'days_until_deadline': conference.days_until_deadline(),
            'is_submission_open': conference.is_submission_open(),
            'is_review_open': conference.is_review_open(),
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def tracks(self, request, pk=None):
        """Lấy tracks của conference"""
        conference = self.get_object()
        tracks = conference.tracks.filter(is_active=True)
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)


class TrackViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Track
    """
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsChairOrAdmin()]
    
    def get_queryset(self):
        queryset = Track.objects.filter(is_active=True)
        
        # Filter by conference
        conference_id = self.request.query_params.get('conference')
        if conference_id:
            queryset = queryset.filter(conference_id=conference_id)
        
        return queryset.select_related('conference', 'chair')


class TopicViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Topic
    """
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsChairOrAdmin()]
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Lấy topics phổ biến"""
        # Note: Cần có relationship với papers để count
        topics = Topic.objects.filter(is_active=True).order_by('name')[:50]
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class PolicySettingViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Policy Settings
    """
    queryset = PolicySetting.objects.all()
    serializer_class = PolicySettingSerializer
    permission_classes = [IsChairOrAdmin]
    
    def get_queryset(self):
        queryset = PolicySetting.objects.all()
        
        # Filter by conference
        conference_id = self.request.query_params.get('conference')
        if conference_id:
            queryset = queryset.filter(conference_id=conference_id)
        
        return queryset.select_related('conference')