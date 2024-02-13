from django.apps import AppConfig


if __name__ == "mand_base.mandapp.apps" :
    class MandappConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'mand_base.mandapp'
else :
    class MandappConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'mandapp'
