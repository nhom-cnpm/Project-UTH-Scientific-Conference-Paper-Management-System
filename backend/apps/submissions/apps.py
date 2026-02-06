from django.apps import AppConfig


class SubmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'submissions'
    verbose_name = 'Paper Submissions'
    
    def ready(self):
        """Import signals khi app ready"""
        # import submissions.signals  # Nếu có
        pass
