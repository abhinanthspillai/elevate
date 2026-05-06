from django import forms
from .models import PersonalTask

class PersonalTaskForm(forms.ModelForm):
    class Meta:
        model = PersonalTask
        fields = ['title', 'description', 'due_date', 'priority', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
