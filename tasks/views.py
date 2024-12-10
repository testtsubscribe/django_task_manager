from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

@login_required
def task_list(request):
    # Determine if the user is an admin
    is_admin = request.user.groups.filter(name='admin').exists()

    # Base queryset; admins can see all tasks, others can only see assigned tasks
    if is_admin:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_users=request.user)

    # Get filter parameters
    filter_param = request.GET.get('filter', 'all')
    title_filter = request.GET.get('title', '')

    # Filter tasks based on status
    if filter_param == 'completed':
        tasks = tasks.filter(status=True)
    elif filter_param == 'pending':
        tasks = tasks.filter(status=False)

    # Filter tasks based on title if provided
    if title_filter:
        tasks = tasks.filter(title__icontains=title_filter)

    context = {
        'tasks': tasks,
        'filter': filter_param,
        'title_filter': title_filter,  # Include title filter in context
        'is_admin': is_admin,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def mark_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.groups.filter(name='admin').exists() or request.user in task.assigned_users.all():
        task.status = True
        task.completed_at = timezone.now()
        task.completed_by = request.user
        task.save()
    return redirect('task_list')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')