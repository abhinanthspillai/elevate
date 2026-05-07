from django.shortcuts import render, redirect
import json
from django.contrib.auth.decorators import login_required
from accounts.models import User
from challenges.models import Challenge, ChallengeParticipant, TaskCompletion, Category
from tasks.models import PersonalTask
from django.db.models import Count, Q

def home(request):
    featured_challenges = Challenge.objects.all().order_by('-created_at')[:3]
    top_mentors = User.objects.filter(role='mentor').annotate(num_challenges=Count('created_challenges')).order_by('-num_challenges')[:4]
    stats = {
        'total_users': User.objects.filter(role='user').count(),
        'total_mentors': User.objects.filter(role='mentor').count(),
        'total_challenges': Challenge.objects.count(),
    }
    return render(request, 'dashboard/home.html', {
        'featured_challenges': featured_challenges,
        'top_mentors': top_mentors,
        'stats': stats
    })

@login_required
def index(request):
    if request.user.role == 'admin':
        return redirect('dashboard:admin_dashboard')
    elif request.user.role == 'mentor':
        return redirect('dashboard:mentor_dashboard')
    else:
        return redirect('dashboard:user_dashboard')

@login_required
def user_dashboard(request):
    personal_tasks = PersonalTask.objects.filter(user=request.user)
    joined_challenges = ChallengeParticipant.objects.filter(user=request.user)
    
    total_personal = personal_tasks.count()
    completed_personal = personal_tasks.filter(status='Completed').count()
    
    # Simple chart data: Personal Tasks Completion
    chart_labels = ['Completed', 'Pending']
    chart_data = [completed_personal, total_personal - completed_personal]
    
    recent_activity = TaskCompletion.objects.filter(user=request.user).select_related('task').order_by('-completed_date')[:5]
    pending_tasks = personal_tasks.filter(status='Pending').order_by('due_date')[:5]

    context = {
        'total_personal': total_personal,
        'completed_personal': completed_personal,
        'total_joined': joined_challenges.count(),
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'recent_activity': recent_activity,
        'pending_tasks': pending_tasks,
    }
    return render(request, 'dashboard/user_dashboard.html', context)

@login_required
def mentor_dashboard(request):
    if request.user.role != 'mentor' and request.user.role != 'admin':
        return redirect('dashboard:user_dashboard')
        
    my_challenges = Challenge.objects.filter(mentor=request.user)
    total_challenges = my_challenges.count()
    total_participants = ChallengeParticipant.objects.filter(challenge__mentor=request.user).count()
    
    # Stats for chart
    # Let's say top 5 challenges by participants
    top_challenges = my_challenges.annotate(num_parts=Count('participants')).order_by('-num_parts')[:5]
    chart_labels = [c.title for c in top_challenges]
    chart_data = [c.num_parts for c in top_challenges]

    context = {
        'total_challenges': total_challenges,
        'total_participants': total_participants,
        'my_challenges': my_challenges,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard/mentor_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard:index')
        
    categories = Category.objects.annotate(num_challenges=Count('challenges'))
    context = {
        'total_users': User.objects.filter(role='user').count(),
        'total_mentors': User.objects.filter(role='mentor').count(),
        'total_challenges': Challenge.objects.count(),
        'most_active_category': categories.order_by('-num_challenges').first(),
        # Chart: Challenges per Category
        'categories_labels': [c.name for c in categories],
        'categories_data': [c.num_challenges for c in categories],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
