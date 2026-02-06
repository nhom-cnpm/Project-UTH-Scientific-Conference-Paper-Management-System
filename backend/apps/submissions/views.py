from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Paper, PaperAuthor, PaperVersion, CameraReadySubmission, Metadata
from .services import PaperService
from accounts.permissions import IsOwnerOrAdmin

# Create your views here.

class PaperViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Paper
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin/Chair thấy tất cả
        if user.is_staff or user.is_superuser:
            queryset = Paper.objects.filter(is_deleted=False)
        else:
            # User thấy papers của mình hoặc là author
            queryset = Paper.objects.filter(
                Q(submitter=user) | Q(authors=user),
                is_deleted=False
            ).distinct()
        
        # Filter by conference
        conference_id = self.request.query_params.get('conference')
        if conference_id:
            queryset = queryset.filter(conference_id=conference_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(abstract__icontains=search) |
                Q(keywords__icontains=search)
            )
        
        return queryset.select_related('conference', 'track', 'submitter')
    
    @action(detail=False, methods=['get'])
    def my_papers(self, request):
        """Lấy papers của user hiện tại"""
        papers = PaperService.get_user_papers(request.user)
        
        # Serialize và return
        data = [
            {
                'paper_id': p.paper_id,
                'title': p.title,
                'conference': p.conference.name,
                'status': p.status,
                'submitted_at': p.submitted_at,
                'created_at': p.created_at,
            }
            for p in papers
        ]
        
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit paper"""
        paper = self.get_object()
        
        try:
            PaperService.submit_paper(paper, request.user)
            return Response({
                'status': 'success',
                'message': 'Paper submitted successfully'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        """Withdraw paper"""
        paper = self.get_object()
        
        if paper.submitter != request.user:
            return Response(
                {'error': 'Only submitter can withdraw'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            paper.withdraw()
            return Response({
                'status': 'success',
                'message': 'Paper withdrawn'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def add_author(self, request, pk=None):
        """Thêm author"""
        paper = self.get_object()
        
        author_id = request.data.get('author_id')
        order = request.data.get('order', paper.authors.count() + 1)
        is_corresponding = request.data.get('is_corresponding', False)
        
        try:
            from accounts.models import User
            author = User.objects.get(id=author_id)
            
            PaperService.add_author(paper, author, order, is_corresponding)
            
            return Response({
                'status': 'success',
                'message': 'Author added'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def upload_version(self, request, pk=None):
        """Upload version mới"""
        paper = self.get_object()
        
        pdf_file = request.FILES.get('pdf_file')
        changes_summary = request.data.get('changes_summary', '')
        
        if not pdf_file:
            return Response(
                {'error': 'PDF file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            version = PaperService.upload_new_version(
                paper, pdf_file, request.user, changes_summary
            )
            
            return Response({
                'status': 'success',
                'version_number': version.version_number
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """Lấy version history"""
        paper = self.get_object()
        versions = paper.versions.all()
        
        data = [
            {
                'version_id': v.version_id,
                'version_number': v.version_number,
                'uploaded_by': v.uploaded_by.email,
                'uploaded_at': v.uploaded_at,
                'changes_summary': v.changes_summary,
            }
            for v in versions
        ]
        
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def check_plagiarism(self, request, pk=None):
        """Check plagiarism"""
        paper = self.get_object()
        
        try:
            score = PaperService.check_plagiarism(paper)
            
            return Response({
                'similarity_score': score,
                'status': 'acceptable' if score < 20 else 'review_needed'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        