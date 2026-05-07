from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from challenges.models import Category, Challenge, ChallengeTask
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial data for the Elevate platform'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin created: admin / admin123'))

        # 2. Create Categories
        category_names = ['Coding', 'Design', 'Fitness', 'Marketing', 'Personal Growth']
        categories = {}
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories[name] = cat

        # 3. Create a Mentor
        mentor, created = User.objects.get_or_create(
            username='mentor_sarah',
            defaults={'role': 'mentor'}
        )
        if created:
            mentor.set_password('mentor123')
            mentor.save()

        # 4. Create Sample Challenges
        if not Challenge.objects.filter(title='30 Days of Python').exists():
            c1 = Challenge.objects.create(
                title='30 Days of Python',
                description='Master Python basics with daily challenges.',
                category=categories['Coding'],
                mentor=mentor,
                difficulty='Easy',
                duration_days=30
            )
            ChallengeTask.objects.create(challenge=c1, day_number=1, task_title='Environment Setup', task_description='Install Python and VS Code.')
            ChallengeTask.objects.create(challenge=c1, day_number=2, task_title='Data Types', task_description='Learn about Strings and Integers.')
            self.stdout.write('Created Python Challenge')

        if not Challenge.objects.filter(title='7-Day Fitness Blitz').exists():
            c2 = Challenge.objects.create(
                title='7-Day Fitness Blitz',
                description='Kickstart your health with these quick workouts.',
                category=categories['Fitness'],
                mentor=mentor,
                difficulty='Medium',
                duration_days=7
            )
            ChallengeTask.objects.create(challenge=c2, day_number=1, task_title='Full Body Warmup', task_description='10 minutes of jumping jacks and stretching.')
            self.stdout.write('Created Fitness Challenge')

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))

