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
        else:
            self.stdout.write('Admin already exists.')

        # 2. Create Categories
        categories = ['Coding', 'Design', 'Fitness', 'Marketing', 'Personal Growth']
        cat_objs = []
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(name=cat_name)
            cat_objs.append(cat)
            if created:
                self.stdout.write(f'Category created: {cat_name}')

        # 3. Create a Mentor
        mentor, created = User.objects.get_or_create(
            username='mentor_john',
            defaults={'role': 'mentor'}
        )
        if created:
            mentor.set_password('mentor123')
            mentor.save()

        # 4. Create Sample Challenge
        if not Challenge.objects.exists():
            challenge = Challenge.objects.create(
                title='30 Days of Python',
                description='Master Python basics with daily challenges.',
                category=cat_objs[0],
                mentor=mentor
            )
            ChallengeTask.objects.create(
                challenge=challenge,
                day_number=1,
                task_title='Install Python and Hello World',
                task_description='Set up your environment and run your first script.'
            )
            ChallengeTask.objects.create(
                challenge=challenge,
                day_number=2,
                task_title='Variables and Types',
                task_description='Learn about integers, strings, and floats.'
            )
            self.stdout.write(self.style.SUCCESS('Sample challenge created.'))

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
