from django.apps import AppConfig


class ProceedingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proceedings'
    verbose_name = 'Conference Proceedings'
    
    def ready(self):
        """Import signals khi app ready"""
        # import proceedings.signals  # Nếu có
        pass