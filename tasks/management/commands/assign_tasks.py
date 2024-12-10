from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task

class Command(BaseCommand):
    help = 'Assign all non-superuser users to all tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output'
        )

    def handle(self, *args, **options):
        verbose = options['verbose']

        # Get all non-superuser users
        users = User.objects.filter(is_superuser=False)
        
        # Get all tasks
        tasks = Task.objects.all()

        # Track assignments
        total_assignments = 0
        skipped_assignments = 0

        # Assign each user to each task
        for task in tasks:
            for user in users:
                # Check if assignment already exists
                if not task.assigned_users.filter(id=user.id).exists():
                    # Add user to task
                    task.assigned_users.add(user)
                    total_assignments += 1
                    
                    if verbose:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Assigned task '{task.title}' to user '{user.username}'"
                            )
                        )
                else:
                    skipped_assignments += 1

        # Print summary
        if verbose:
            self.stdout.write(f"\nTotal new assignments: {total_assignments}")
            self.stdout.write(f"Skipped duplicate assignments: {skipped_assignments}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Task assignment completed. {total_assignments} new assignments made."
            )
        )
