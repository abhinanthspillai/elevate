from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Challenge(models.Model):
    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_challenges')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='challenges')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    duration_days = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ChallengeTask(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='tasks')
    day_number = models.PositiveIntegerField()
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()

    def __str__(self):
        return f"{self.challenge.title} - Day {self.day_number}: {self.task_title}"

class ChallengeParticipant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='joined_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} joined {self.challenge.title}"

class TaskCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_completions')
    task = models.ForeignKey(ChallengeTask, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.task_title} - {self.completed}"
