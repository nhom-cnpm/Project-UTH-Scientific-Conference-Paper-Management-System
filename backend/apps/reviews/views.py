from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import ReviewAssignment, Review, ReviewDiscussion
from .services import ReviewAssignmentService, ReviewService, ReviewDiscussionService
from .permissions import IsReviewerOrChair, IsChairOnly

# Create your views here.
class ReviewAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Review Assignment
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Chair/Admin thấy tất cả
        if user.groups.filter(name__in=['Chair', 'Admin']).exists():
            return ReviewAssignment.objects.all().select_related(
                'paper', 'reviewer', 'assigned_by'
            )
        
        # Reviewer chỉ thấy của mình
        return ReviewAssignment.objects.filter(
            reviewer=user
        ).select_related('paper', 'assigned_by')
    
    @action(detail=False, methods=['get'])
    def my_assignments(self, request):
        """Lấy assignments của reviewer hiện tại"""
        assignments = ReviewAssignmentService.get_reviewer_assignments(
            request.user
        )
        
        return Response({
            'pending': list(assignments.filter(status='pending').values()),
            'accepted': list(assignments.filter(status='accepted').values()),
            'declined': list(assignments.filter(status='declined').values()),
        })
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Reviewer accept assignment"""
        assignment = self.get_object()
        
        if assignment.reviewer != request.user:
            return Response(
                {'error': 'Bạn không có quyền accept assignment này'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            assignment.accept()
            return Response({
                'status': 'success',
                'message': 'Assignment đã được accept',
                'data': {
                    'assignment_id': assignment.assignment_id,
                    'status': assignment.status,
                }
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Reviewer decline assignment"""
        assignment = self.get_object()
        
        if assignment.reviewer != request.user:
            return Response(
                {'error': 'Bạn không có quyền decline assignment này'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reason = request.data.get('reason', '')
        
        try:
            assignment.decline(reason)
            return Response({
                'status': 'success',
                'message': 'Assignment đã được decline',
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def declare_coi(self, request, pk=None):
        """Khai báo Conflict of Interest"""
        assignment = self.get_object()
        
        if assignment.reviewer != request.user:
            return Response(
                {'error': 'Bạn không có quyền khai báo COI cho assignment này'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reason = request.data.get('reason', '')
        if not reason:
            return Response(
                {'error': 'Vui lòng cung cấp lý do COI'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            assignment.declare_coi(reason)
            return Response({
                'status': 'success',
                'message': 'COI đã được khai báo',
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Review
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Chair thấy tất cả
        if user.groups.filter(name__in=['Chair', 'Admin']).exists():
            return Review.objects.filter(is_deleted=False).select_related(
                'assignment__reviewer', 'assignment__paper'
            )
        
        # Reviewer chỉ thấy của mình
        return Review.objects.filter(
            assignment__reviewer=user,
            is_deleted=False
        ).select_related('assignment__paper')
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Lấy reviews của reviewer hiện tại"""
        reviews = self.get_queryset().filter(
            assignment__reviewer=request.user
        )
        
        return Response({
            'draft': list(reviews.filter(status='draft').values()),
            'submitted': list(reviews.filter(status='submitted').values()),
            'finalized': list(reviews.filter(status='finalized').values()),
        })
    
    def create(self, request, *args, **kwargs):
        """Tạo review mới"""
        assignment_id = request.data.get('assignment_id')
        
        try:
            assignment = ReviewAssignment.objects.get(
                assignment_id=assignment_id,
                reviewer=request.user
            )
        except ReviewAssignment.DoesNotExist:
            return Response(
                {'error': 'Assignment không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            review = ReviewService.create_review(
                assignment=assignment,
                score=request.data.get('score'),
                recommendation=request.data.get('recommendation'),
                confidence_level=request.data.get('confidence_level', 2),
                content_review=request.data.get('content_review', ''),
                comment_to_author=request.data.get('comment_to_author', ''),
                comment_to_chair=request.data.get('comment_to_chair', ''),
            )
            
            return Response({
                'status': 'success',
                'review_id': review.review_id,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit review"""
        review = self.get_object()
        
        if review.assignment.reviewer != request.user:
            return Response(
                {'error': 'Bạn không có quyền submit review này'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            ReviewService.submit_review(review)
            return Response({
                'status': 'success',
                'message': 'Review đã được submit',
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsChairOnly])
    def finalize(self, request, pk=None):
        """Finalize review - Chair only"""
        review = self.get_object()
        
        try:
            review.finalize()
            return Response({
                'status': 'success',
                'message': 'Review đã được finalized',
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReviewDiscussionViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho Review Discussion
    """
    permission_classes = [IsAuthenticated, IsReviewerOrChair]
    
    def get_queryset(self):
        return ReviewDiscussion.objects.filter(
            is_deleted=False
        ).select_related('review', 'user', 'parent')
    
    def perform_create(self, serializer):
        """Auto set user khi tạo discussion"""
        serializer.save(user=self.request.user)