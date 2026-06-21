import json
import os
from datetime import datetime
from pathlib import Path

class TaskManager:
    def __init__(self):
        self.tasks_file = Path(__file__).parent / "tasks.json"
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(self, title, priority, due_date):
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'priority': priority,
            'due_date': due_date,
            'status': 'pending',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def complete_task(self, task_index):
        if task_index < len(self.tasks):
            self.tasks[task_index]['status'] = 'completed'
            self.tasks[task_index]['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_tasks()
    
    def delete_task(self, task_index):
        if task_index < len(self.tasks):
            self.tasks.pop(task_index)
            self.save_tasks()
    
    def get_pending_tasks(self):
        return [t for t in self.tasks if t['status'] == 'pending']
    
    def get_completed_tasks(self):
        return [t for t in self.tasks if t['status'] == 'completed']
    
    def get_overdue_tasks(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return [t for t in self.tasks if t['status'] == 'pending' and t['due_date'] < today]