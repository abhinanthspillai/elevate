from django.shortcuts import render
from accounts.models import User
from challenges.models import ChallengeParticipant, TaskCompletion
from tasks.models import PersonalTask
from django.db.models import Count

from django.db.models import Count, Q, F

def leaderboard(request):
    # Calculate all points in a single database query using annotations
    # Points: Challenge Task (10), Personal Task (5), Challenge Participation (20)
    users_with_stats = User.objects.filter(role='user').annotate(
        cp=Count('taskcompletion', filter=Q(taskcompletion__completed=True), distinct=True),
        pp=Count('personaltask', filter=Q(personaltask__status='Completed'), distinct=True),
        partp=Count('joined_challenges', distinct=True)
    ).annotate(
        challenge_points=F('cp') * 10,
        personal_points=F('pp') * 5,
        participation_points=F('partp') * 20
    ).annotate(
        total_points=F('challenge_points') + F('personal_points') + F('participation_points')
    ).order_by('-total_points')

    leaderboard_data = []
    for i, user in enumerate(users_with_stats):
        leaderboard_data.append({
            'user': user,
            'total_points': user.total_points,
            'challenge_points': user.challenge_points,
            'personal_points': user.personal_points,
            'participation_points': user.participation_points,
            'rank': i + 1
        })
        
    return render(request, 'leaderboard/list.html', {'leaderboard': leaderboard_data})
