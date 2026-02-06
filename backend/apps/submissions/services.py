from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Paper, PaperAuthor, PaperVersion, SubmissionActivity

class PaperService:
    """Service để quản lý papers"""
    
    @staticmethod
    @transaction.atomic
    def create_paper(conference, submitter, title, abstract, **kwargs):
        """Tạo paper mới"""
        # Check if conference accepts submissions
        if not conference.is_submission_open():
            raise ValidationError("Conference is not accepting submissions")
        
        # Create paper
        paper = Paper.objects.create(
            conference=conference,
            submitter=submitter,
            title=title,
            abstract=abstract,
            status='draft',
            **kwargs
        )
        
        # Add submitter as first author
        PaperAuthor.objects.create(
            paper=paper,
            author=submitter,
            order=1,
            is_corresponding=True
        )
        
        # Log activity
        SubmissionActivity.objects.create(
            paper=paper,
            activity_type='created',
            user=submitter,
            description=f"Paper created: {title}"
        )
        
        return paper
    
    @staticmethod
    @transaction.atomic
    def submit_paper(paper, user):
        """Submit paper cho review"""
        # Validation
        if paper.submitter != user:
            raise ValidationError("Only submitter can submit the paper")
        
        if paper.status != 'draft':
            raise ValidationError("Can only submit papers in draft status")
        
        # Submit
        paper.submit()
        
        # Log activity
        SubmissionActivity.objects.create(
            paper=paper,
            activity_type='submitted',
            user=user,
            description="Paper submitted for review"
        )
        
        return paper
    
    @staticmethod
    @transaction.atomic
    def add_author(paper, author, order, is_corresponding=False):
        """Thêm author vào paper"""
        # Check if already exists
        if PaperAuthor.objects.filter(paper=paper, author=author).exists():
            raise ValidationError("Author already added to this paper")
        
        # Add author
        paper_author = PaperAuthor.objects.create(
            paper=paper,
            author=author,
            order=order,
            is_corresponding=is_corresponding
        )
        
        # Log activity
        SubmissionActivity.objects.create(
            paper=paper,
            activity_type='author_added',
            user=paper.submitter,
            description=f"Author added: {author.full_name or author.email}",
            metadata={'author_id': author.id, 'order': order}
        )
        
        return paper_author
    
    @staticmethod
    @transaction.atomic
    def remove_author(paper, author):
        """Xóa author khỏi paper"""
        try:
            paper_author = PaperAuthor.objects.get(paper=paper, author=author)
            
            # Cannot remove if only one author
            if paper.authors.count() <= 1:
                raise ValidationError("Cannot remove the only author")
            
            paper_author.delete()
            
            # Log activity
            SubmissionActivity.objects.create(
                paper=paper,
                activity_type='author_removed',
                user=paper.submitter,
                description=f"Author removed: {author.full_name or author.email}",
                metadata={'author_id': author.id}
            )
            
            return True
        except PaperAuthor.DoesNotExist:
            raise ValidationError("Author not found in this paper")
    
    @staticmethod
    @transaction.atomic
    def upload_new_version(paper, pdf_file, user, changes_summary=""):
        """Upload version mới của paper"""
        # Get next version number
        latest_version = paper.versions.first()
        next_version = latest_version.version_number + 1 if latest_version else 1
        
        # Create new version
        version = PaperVersion.objects.create(
            paper=paper,
            version_number=next_version,
            pdf_file=pdf_file,
            changes_summary=changes_summary,
            uploaded_by=user
        )
        
        # Update paper's main file
        paper.pdf_file = pdf_file
        paper.save()
        
        # Log activity
        SubmissionActivity.objects.create(
            paper=paper,
            activity_type='file_uploaded',
            user=user,
            description=f"New version uploaded: v{next_version}",
            metadata={'version': next_version}
        )
        
        return version
    
    @staticmethod
    def get_user_papers(user, conference=None, status=None):
        """Lấy papers của user"""
        queryset = Paper.objects.filter(
            submitter=user,
            is_deleted=False
        ).select_related('conference', 'track')
        
        if conference:
            queryset = queryset.filter(conference=conference)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_conference_papers(conference, status=None):
        """Lấy tất cả papers của conference"""
        queryset = Paper.objects.filter(
            conference=conference,
            is_deleted=False
        ).select_related('submitter', 'track')
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-submitted_at')
    
    @staticmethod
    def check_plagiarism(paper):
        """Check plagiarism (placeholder - cần integrate với service thật)"""
        # TODO: Integrate với plagiarism detection service
        # For now, return dummy score
        import random
        similarity_score = random.uniform(0, 15)  # 0-15% is acceptable
        
        paper.ai_similarity_score = similarity_score
        paper.save()
        
        return similarity_score