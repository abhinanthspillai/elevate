from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Challenge, ChallengeTask, Category, ChallengeParticipant, TaskCompletion
from .forms import ChallengeForm, ChallengeTaskForm
from django.contrib import messages
from django.utils import timezone

def challenge_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    challenges = Challenge.objects.all()
    
    if query:
        challenges = challenges.filter(title__icontains=query)
    if category_id:
        challenges = challenges.filter(category_id=category_id)
        
    categories = Category.objects.all()
    return render(request, 'challenges/list.html', {'challenges': challenges, 'categories': categories})

@login_required
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    is_joined = ChallengeParticipant.objects.filter(user=request.user, challenge=challenge).exists()
    tasks = challenge.tasks.all().order_by('day_number')
    
    completions = {}
    if is_joined:
        comp_list = TaskCompletion.objects.filter(user=request.user, task__challenge=challenge)
        completions = {c.task_id: c.completed for c in comp_list}
        
    return render(request, 'challenges/detail.html', {
        'challenge': challenge,
        'is_joined': is_joined,
        'tasks': tasks,
        'completions': completions
    })

@login_required
def join_challenge(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    ChallengeParticipant.objects.get_or_create(user=request.user, challenge=challenge)
    messages.success(request, f"You have joined {challenge.title}!")
    return redirect('challenges:detail', pk=pk)

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(ChallengeTask, id=task_id)
    completion, created = TaskCompletion.objects.get_or_create(user=request.user, task=task)
    completion.completed = True
    completion.completed_date = timezone.now()
    completion.save()
    messages.success(request, f"Task '{task.task_title}' completed!")
    return redirect('challenges:detail', pk=task.challenge.id)

# Mentor/Admin CRUD
@login_required
def challenge_create(request):
    if request.user.role not in ['mentor', 'admin']:
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.mentor = request.user
            challenge.save()
            messages.success(request, "Challenge created successfully!")
            return redirect('challenges:manage_tasks', pk=challenge.pk)
    else:
        form = ChallengeForm()
    return render(request, 'challenges/form.html', {'form': form, 'title': 'Create Challenge'})

@login_required
def challenge_edit(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    if request.user != challenge.mentor and request.user.role != 'admin':
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, "Challenge updated!")
            return redirect('challenges:detail', pk=pk)
    else:
        form = ChallengeForm(instance=challenge)
    return render(request, 'challenges/form.html', {'form': form, 'title': 'Edit Challenge'})

@login_required
def challenge_delete(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    if request.user != challenge.mentor and request.user.role != 'admin':
        return redirect('dashboard:index')
    challenge.delete()
    messages.success(request, "Challenge deleted!")
    return redirect('dashboard:mentor_dashboard')

@login_required
def manage_tasks(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    if request.user != challenge.mentor and request.user.role != 'admin':
        return redirect('dashboard:index')
    
    tasks = challenge.tasks.all().order_by('day_number')
    if request.method == 'POST':
        form = ChallengeTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.challenge = challenge
            task.save()
            messages.success(request, "Task added!")
            return redirect('challenges:manage_tasks', pk=pk)
    else:
        form = ChallengeTaskForm()
        
    return render(request, 'challenges/manage_tasks.html', {
        'challenge': challenge,
        'tasks': tasks,
        'form': form
    })

@login_required
def task_edit(request, pk):
    task = get_object_or_404(ChallengeTask, pk=pk)
    if request.user != task.challenge.mentor and request.user.role != 'admin':
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = ChallengeTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated!")
            return redirect('challenges:manage_tasks', pk=task.challenge.pk)
    else:
        form = ChallengeTaskForm(instance=task)
    return render(request, 'challenges/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(ChallengeTask, pk=pk)
    challenge_id = task.challenge.id
    if request.user != task.challenge.mentor and request.user.role != 'admin':
        return redirect('dashboard:index')
    task.delete()
    messages.success(request, "Task deleted!")
    return redirect('challenges:manage_tasks', pk=challenge_id)
