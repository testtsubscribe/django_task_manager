import os
import sys
import argparse
import django

def setup_django():
    """
    Setup Django environment to use Django ORM outside of manage.py
    """
    # Get the project root directory (assuming this script is in the same directory as manage.py)
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
    
    # Initialize Django
    django.setup()

def assign_users_to_tasks(verbose=False):
    """
    Assign all non-superuser users to all tasks
    
    :param verbose: If True, print detailed information about assignments
    """
    from django.contrib.auth.models import User
    from tasks.models import Task  # Adjust import based on your app name
    
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
                    print(f"Assigned task '{task.title}' to user '{user.username}'")
            else:
                skipped_assignments += 1
    
    # Print summary
    if verbose:
        print(f"\nTotal new assignments: {total_assignments}")
        print(f"Skipped duplicate assignments: {skipped_assignments}")
    
    return total_assignments, skipped_assignments

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Assign users to tasks')
    parser.add_argument('-v', '--verbose', 
                        action='store_true', 
                        help='Enable verbose output')
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Setup Django environment
        setup_django()
        
        # Run the assignment
        total, skipped = assign_users_to_tasks(verbose=args.verbose)
        
        print(f"Task assignment completed. {total} new assignments made.")
        sys.exit(0)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()