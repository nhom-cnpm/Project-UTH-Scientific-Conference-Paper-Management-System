from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Proceedings, ProceedingsEntry, Section
from .services import ProceedingsService
from conferences.models import Conference
from accounts.permissions import IsChairOrAdmin

# Create your views here.
class ProceedingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Proceedings
    """
    queryset = Proceedings.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'table_of_contents']:
            return [IsAuthenticated()]
        return [IsChairOrAdmin()]
    
    def get_queryset(self):
        queryset = Proceedings.objects.filter(is_deleted=False)
        
        # Filter by conference
        conference_id = self.request.query_params.get('conference')
        if conference_id:
            queryset = queryset.filter(conference_id=conference_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.select_related('conference')
    
    @action(detail=True, methods=['get'])
    def table_of_contents(self, request, pk=None):
        """Get table of contents"""
        proceedings = self.get_object()
        
        toc = ProceedingsService.generate_table_of_contents(proceedings)
        
        return Response({
            'proceedings_title': proceedings.title,
            'total_papers': proceedings.total_papers,
            'entries': toc
        })
    
    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        """Get organized by sections"""
        proceedings = self.get_object()
        
        organized = ProceedingsService.organize_by_sections(proceedings)
        
        return Response(organized)
    
    @action(detail=True, methods=['post'], permission_classes=[IsChairOrAdmin])
    def publish(self, request, pk=None):
        """Publish proceedings"""
        proceedings = self.get_object()
        
        try:
            ProceedingsService.publish_proceedings(proceedings)
            return Response({
                'status': 'success',
                'message': 'Proceedings published successfully'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsChairOrAdmin])
    def assign_pages(self, request, pk=None):
        """Assign page numbers"""
        proceedings = self.get_object()
        start_page = request.data.get('start_page', 1)
        
        try:
            ProceedingsService.assign_page_numbers(proceedings, start_page)
            return Response({
                'status': 'success',
                'message': 'Page numbers assigned'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics"""
        proceedings = self.get_object()
        
        return Response({
            'total_papers': proceedings.total_papers,
            'total_pages': proceedings.total_pages,
            'status': proceedings.status,
            'publication_date': proceedings.publication_date,
        })


class ProceedingsEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Proceedings Entry
    """
    queryset = ProceedingsEntry.objects.all()
    permission_classes = [IsChairOrAdmin]
    
    def get_queryset(self):
        queryset = ProceedingsEntry.objects.all()
        
        # Filter by proceedings
        proceedings_id = self.request.query_params.get('proceedings')
        if proceedings_id:
            queryset = queryset.filter(proceedings_id=proceedings_id)
        
        # Filter by section
        section = self.request.query_params.get('section')
        if section:
            queryset = queryset.filter(section=section)
        
        return queryset.select_related('proceedings', 'paper')
    
    @action(detail=True, methods=['post'])
    def generate_doi(self, request, pk=None):
        """Generate DOI for entry"""
        entry = self.get_object()
        
        doi = entry.generate_doi()
        
        if doi:
            return Response({
                'status': 'success',
                'doi': doi
            })
        else:
            return Response(
                {'error': 'DOI prefix not configured for proceedings'},
                status=status.HTTP_400_BAD_REQUEST
            )