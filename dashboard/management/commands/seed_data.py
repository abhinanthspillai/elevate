from django.core.management.base import BaseCommand
from accounts.models import User
from challenges.models import Category, Challenge, ChallengeTask
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        # Create Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
            self.stdout.write(self.style.SUCCESS('Admin created: admin / admin123'))

        # Create Mentor
        mentor, created = User.objects.get_or_create(username='mentor1', defaults={'email': 'mentor@example.com', 'role': 'mentor'})
        if created:
            mentor.set_password('mentor123')
            mentor.save()
            self.stdout.write(self.style.SUCCESS('Mentor created: mentor1 / mentor123'))

        # Create User
        user, created = User.objects.get_or_create(username='user1', defaults={'email': 'user@example.com', 'role': 'user'})
        if created:
            user.set_password('user123')
            user.save()
            self.stdout.write(self.style.SUCCESS('User created: user1 / user123'))

        # Create Categories
        categories = ['Programming', 'Fitness', 'Mindfulness', 'Career']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)

        # Create a Challenge
        prog_cat = Category.objects.get(name='Programming')
        challenge, created = Challenge.objects.get_or_create(
            title='30 Days of Python',
            defaults={
                'description': 'A comprehensive challenge to master Python basics.',
                'mentor': mentor,
                'category': prog_cat,
                'difficulty': 'Medium',
                'duration_days': 30
            }
        )

        if created:
            # Create Tasks for the challenge
            ChallengeTask.objects.create(challenge=challenge, day_number=1, task_title='Environment Setup', task_description='Install Python and VS Code.')
            ChallengeTask.objects.create(challenge=challenge, day_number=2, task_title='Variables & Types', task_description='Learn about integers, strings, and floats.')
            ChallengeTask.objects.create(challenge=challenge, day_number=3, task_title='Control Flow', task_description='Practice if-else statements.')
            self.stdout.write(self.style.SUCCESS('Seed data populated!'))
