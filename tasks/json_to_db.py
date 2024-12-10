#"""

import sqlite3
import json
from datetime import datetime
import os


def import_tasks_from_json(json_file_path):
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    current_directory = os.getcwd()
    up_directory = os.path.abspath(os.path.join(current_directory, '..'))
    #root_directory = os.path.abspath(os.path.join(current_directory, '..', '..'))

    sqlite3_path = os.path.join(up_directory, 'db.sqlite3')


    # Connect to SQLite database
    conn = sqlite3.connect(sqlite3_path)
    cursor = conn.cursor()
    
    # Get column names from the tasks_task table
    cursor.execute("PRAGMA table_info(tasks_task)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Remove 'id' from columns as it's auto-generated
    if 'id' in columns:
        columns.remove('id')
    
    # Prepare SQL statement
    placeholders = ','.join(['?' for _ in columns])
    columns_str = ','.join(columns)
    sql = f"INSERT INTO tasks_task ({columns_str}) VALUES ({placeholders})"
    
    # Insert each task
    inserted_count = 0
    for task in tasks:
        # Remove id field from task data
        if 'id' in task:
            del task['id']
            
        # Extract values in the same order as columns
        values = [task.get(column) for column in columns]
        
        try:
            cursor.execute(sql, values)
            inserted_count += 1
        except sqlite3.Error as e:
            print(f"Error inserting task: {e}")
            continue
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    return inserted_count

if __name__ == "__main__":
    current_directory = os.getcwd()
    # You can specify the JSON file path as an argument
    json_file_path = os.path.join(current_directory, 'tasks_to_import.json') #'tasks_to_import.json'  # Update this to your JSON file name
    inserted = import_tasks_from_json(json_file_path)
    print(f"Successfully imported {inserted} tasks into the database")

#"""

"""
import os

# Get the current working directory
current_directory = os.getcwd()
print("Current Directory:", current_directory)
#/home/ramil/awesome_projects/test_diff/empty_task_manager/tasks/migrations



# Navigate two folders up
parent_parent_directory = os.path.abspath(os.path.join(current_directory, '..', '..'))
print("\nTwo Folders Up Directory:", parent_parent_directory)

# List contents of the two-folders-up directory
print("\nContents of the two-folders-up directory:")
for item in os.listdir(parent_parent_directory):
    full_path = os.path.join(parent_parent_directory, item)
    if os.path.isdir(full_path):
        print(f"[Folder] {item}")
    else:
        print(f"[File]   {item}")


"""