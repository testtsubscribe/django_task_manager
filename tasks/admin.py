
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'completed_at')
    filter_horizontal = ('assigned_users',)
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at')
'''

from django.contrib import admin
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'Task Manager Administration'
    site_title = 'Task Manager Admin Portal'
    index_title = 'Welcome to Task Manager Admin'

admin_site = CustomAdminSite()
'''