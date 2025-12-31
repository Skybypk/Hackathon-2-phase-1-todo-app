from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
from typing import List, Optional

app = Flask(__name__)

class Todo:
    """Todo model class representing a todo item"""

    def __init__(self, id: int, task: str, completed: bool = False,
                 created_at: str = None, due_date: str = None,
                 priority: str = "medium", category: str = ""):
        self.id = id
        self.task = task
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.due_date = due_date
        self.priority = priority  # high, medium, low
        self.category = category

    def to_dict(self):
        """Convert Todo object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'task': self.task,
            'completed': self.completed,
            'created_at': self.created_at,
            'due_date': self.due_date,
            'priority': self.priority,
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data):
        """Create Todo object from dictionary"""
        return cls(
            id=data['id'],
            task=data['task'],
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            due_date=data.get('due_date'),
            priority=data.get('priority', 'medium'),
            category=data.get('category', '')
        )

class TodoManager:
    """Manages todo items and persistence"""

    def __init__(self, filename: str = 'todos.json'):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self) -> List[Todo]:
        """Load todos from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Todo.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                # If file is corrupted or has old format, return empty list
                return []
        return []

    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([todo.to_dict() for todo in self.todos], f, indent=2)

    def get_next_id(self) -> int:
        """Get the next available ID"""
        if not self.todos:
            return 1
        return max(todo.id for todo in self.todos) + 1

    def add_todo(self, task: str, due_date: str = None,
                 priority: str = "medium", category: str = "") -> Todo:
        """Add a new todo item"""
        new_id = self.get_next_id()
        new_todo = Todo(
            id=new_id,
            task=task,
            due_date=due_date,
            priority=priority,
            category=category
        )
        self.todos.append(new_todo)
        self.save_todos()
        return new_todo

    def update_todo(self, todo_id: int, task: str = None,
                   completed: bool = None, due_date: str = None,
                   priority: str = None, category: str = None) -> Optional[Todo]:
        """Update an existing todo item"""
        for todo in self.todos:
            if todo.id == todo_id:
                if task is not None:
                    todo.task = task
                if completed is not None:
                    todo.completed = completed
                if due_date is not None:
                    todo.due_date = due_date
                if priority is not None:
                    todo.priority = priority
                if category is not None:
                    todo.category = category

                self.save_todos()
                return todo
        return None

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item"""
        original_count = len(self.todos)
        self.todos = [todo for todo in self.todos if todo.id != todo_id]
        if len(self.todos) < original_count:
            self.save_todos()
            return True
        return False

    def get_completed_count(self) -> int:
        """Get count of completed todos"""
        return sum(1 for todo in self.todos if todo.completed)

    def get_total_count(self) -> int:
        """Get total count of todos"""
        return len(self.todos)

    def get_completion_percentage(self) -> int:
        """Get completion percentage"""
        total = self.get_total_count()
        if total == 0:
            return 0
        return int((self.get_completed_count() / total) * 100)

# Initialize todo manager
todo_manager = TodoManager()

@app.route('/')
def index():
    """Main page route"""
    todos = todo_manager.todos
    completion_percentage = todo_manager.get_completion_percentage()
    return render_template('index.html', todos=todos, completion_percentage=completion_percentage)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo"""
    try:
        data = request.get_json()
        task = data.get('task', '').strip()
        due_date = data.get('due_date')
        priority = data.get('priority', 'medium')
        category = data.get('category', '')

        if not task:
            return jsonify({'error': 'Task cannot be empty'}), 400

        new_todo = todo_manager.add_todo(task, due_date, priority, category)
        return jsonify({'success': True, 'todo': new_todo.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    try:
        data = request.get_json()
        updated_todo = todo_manager.update_todo(
            todo_id,
            task=data.get('task'),
            completed=data.get('completed'),
            due_date=data.get('due_date'),
            priority=data.get('priority'),
            category=data.get('category')
        )

        if updated_todo:
            return jsonify({'success': True, 'todo': updated_todo.to_dict()})
        else:
            return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    try:
        success = todo_manager.delete_todo(todo_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/toggle/<int:todo_id>', methods=['PUT'])
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    try:
        # Find the todo to get its current status
        todo = next((t for t in todo_manager.todos if t.id == todo_id), None)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404

        # Update the completion status
        updated_todo = todo_manager.update_todo(todo_id, completed=not todo.completed)
        if updated_todo:
            return jsonify({
                'success': True,
                'todo': updated_todo.to_dict(),
                'completion_percentage': todo_manager.get_completion_percentage()
            })
        else:
            return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export')
def export_todos():
    """Export todos to CSV"""
    try:
        import csv
        from io import StringIO
        from flask import make_response

        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['ID', 'Task', 'Completed', 'Created At', 'Due Date', 'Priority', 'Category'])

        # Write data
        for todo in todo_manager.todos:
            writer.writerow([
                todo.id,
                todo.task,
                todo.completed,
                todo.created_at,
                todo.due_date or '',
                todo.priority,
                todo.category
            ])

        # Create response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=todos.csv'

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def get_stats():
    """Get statistics about todos"""
    try:
        completed = todo_manager.get_completed_count()
        total = todo_manager.get_total_count()
        percentage = todo_manager.get_completion_percentage()

        # Get stats by priority
        priority_stats = {
            'high': sum(1 for t in todo_manager.todos if t.priority == 'high'),
            'medium': sum(1 for t in todo_manager.todos if t.priority == 'medium'),
            'low': sum(1 for t in todo_manager.todos if t.priority == 'low')
        }

        # Get stats by category
        categories = set(t.category for t in todo_manager.todos if t.category)
        category_stats = {cat: sum(1 for t in todo_manager.todos if t.category == cat) for cat in categories}

        return jsonify({
            'completed': completed,
            'total': total,
            'percentage': percentage,
            'priority_stats': priority_stats,
            'category_stats': category_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)