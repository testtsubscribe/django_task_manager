from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create default user groups, admin user, and test data for Task Manager'

    def handle(self, *args, **kwargs):
        # Create default groups
        self.create_groups()
        
        # Create admin user
        self.create_admin_user()
        
        # Create test users
        self.create_test_users()

    def create_groups(self):
        """Create default user groups."""
        groups = ['admin', 'standard_user']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))

    def create_admin_user(self):
        """Create admin user and add to admin group."""
        try:
            admin_user = User.objects.get(username='rln_admin')
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        except User.DoesNotExist:
            admin_user = User.objects.create_superuser(
                username='rln_admin',
                password='admin_pass123',
                email='admin@taskmanager.com'  # Optional: add an email
            )
            admin_group = Group.objects.get(name='admin')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))

    def create_test_users(self):
        """Create test users."""
        test_users = [
            {'username': 'Ramil', 'password': 'R1a2m3i4l'},
            {'username': 'Fatima', 'password': 'F5a4t3i2m1a'},
            {'username': 'Narmin', 'password': 'N3a4r5m6i7n'},
            {'username': 'Nurlan', 'password': 'N9u8r7l6a5n'}
        ]

        for user_data in test_users:
            try:
                User.objects.get(username=user_data['username'])
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))
            except User.DoesNotExist:
                User.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f"Created user: {user_data['username']}"))