# ChallengeHub - Challenge and Productivity Tracking Platform

## Features
- **Authentication**: Custom user roles (User, Mentor, Admin).
- **Dashboards**: Unique dashboard for each role with Chart.js analytics.
- **Challenge Management**: Mentors can create and manage challenges and tasks.
- **Participation**: Users can join challenges and track completion.
- **Personal Tasks**: Full CRUD for individual productivity tracking.
- **Leaderboard**: Gamified ranking system based on platform activity.

## Tech Stack
- **Backend**: Django (Python)
- **Database**: MySQL
- **Frontend**: Bootstrap 5, Font Awesome, Chart.js, Inter Font

## How to Run
1. Create MySQL database `challengehub_db`.
2. Install dependencies: `pip install django mysqlclient pillow`.
3. Migrate: `python manage.py makemigrations accounts challenges tasks ; python manage.py migrate`.
4. Seed data: `python manage.py seed_data`.
5. Run: `python manage.py runserver`.
