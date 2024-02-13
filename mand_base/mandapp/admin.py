from django.contrib import admin

from .models import *


@admin.register(User)
class UserAmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'grade', 'major', 'phone_number']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['btn_text', 'msg_type', 'msg_id', 'creation_datetime', 'added_by', 'finalized', 'deleted']