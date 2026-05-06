from django import forms
from .models import Challenge, ChallengeTask

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'category', 'difficulty', 'duration_days']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ChallengeTaskForm(forms.ModelForm):
    class Meta:
        model = ChallengeTask
        fields = ['day_number', 'task_title', 'task_description']
        widgets = {
            'task_description': forms.Textarea(attrs={'rows': 3}),
        }
