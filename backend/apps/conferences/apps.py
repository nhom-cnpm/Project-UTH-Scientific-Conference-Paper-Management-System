from django.apps import AppConfig



class ConferencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conferences'
    verbose_name = 'Conference Management'
    
    def ready(self):
        """Import signals khi app ready"""
        # import conferences.signals  # Nếu có signals
        pass


