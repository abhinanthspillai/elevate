from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PersonalTask
from .forms import PersonalTaskForm
from django.contrib import messages

@login_required
def task_list(request):
    tasks = PersonalTask.objects.filter(user=request.user).order_by('status', 'due_date')
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = PersonalTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('tasks:list')
    else:
        form = PersonalTaskForm()
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Add Personal Task'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(PersonalTask, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PersonalTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated!")
            return redirect('tasks:list')
    else:
        form = PersonalTaskForm(instance=task)
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(PersonalTask, pk=pk, user=request.user)
    task.delete()
    messages.success(request, "Task deleted!")
    return redirect('tasks:list')

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(PersonalTask, pk=pk, user=request.user)
    task.status = 'Completed' if task.status == 'Pending' else 'Pending'
    task.save()
    return redirect('tasks:list')
