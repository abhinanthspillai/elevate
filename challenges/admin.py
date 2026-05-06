from django.contrib import admin
from .models import Category, Challenge, ChallengeTask, ChallengeParticipant, TaskCompletion

admin.site.register(Category)
admin.site.register(Challenge)
admin.site.register(ChallengeTask)
admin.site.register(ChallengeParticipant)
admin.site.register(TaskCompletion)
