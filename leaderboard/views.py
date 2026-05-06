from django.shortcuts import render
from accounts.models import User
from challenges.models import ChallengeParticipant, TaskCompletion
from tasks.models import PersonalTask
from django.db.models import Count

def leaderboard(request):
    users = User.objects.filter(role='user')
    leaderboard_data = []
    
    for user in users:
        challenge_points = TaskCompletion.objects.filter(user=user, completed=True).count() * 10
        personal_points = PersonalTask.objects.filter(user=user, status='Completed').count() * 5
        participation_points = ChallengeParticipant.objects.filter(user=user).count() * 20
        
        total_points = challenge_points + personal_points + participation_points
        
        leaderboard_data.append({
            'user': user,
            'total_points': total_points,
            'challenge_points': challenge_points,
            'personal_points': personal_points,
            'participation_points': participation_points
        })
        
    # Sort by total points
    leaderboard_data = sorted(leaderboard_data, key=lambda x: x['total_points'], reverse=True)
    
    # Add rank
    for i, data in enumerate(leaderboard_data):
        data['rank'] = i + 1
        
    return render(request, 'leaderboard/list.html', {'leaderboard': leaderboard_data})
