#!/usr/bin/env python3
"""
Console-based Todo application with in-memory storage.
This provides the same functionality as the web version but runs in the terminal.
"""

import json
import os
from datetime import datetime
from typing import List, Optional


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


class TodoConsoleApp:
    """Console-based Todo application with in-memory storage"""

    def __init__(self):
        self.todos = []
        self.next_id = 1
        self.running = True

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        """Display the main menu"""
        print("\n======= TODO APP (Console Version) =======")
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Mark Complete/Incomplete")
        print("4. Delete Todo")
        print("5. Exit")
        print("=========================================")

    def get_user_choice(self):
        """Get and validate user choice"""
        while True:
            try:
                choice = input("Enter your choice (1-5): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                self.running = False
                return '5'

    def add_todo(self):
        """Add a new todo item"""
        print("\n--- Add New Todo ---")
        task = input("Enter the task: ").strip()

        if not task:
            print("Task cannot be empty!")
            return

        # Get priority
        while True:
            priority = input("Enter priority (high/medium/low) [default: medium]: ").strip().lower()
            if priority in ['', 'high', 'medium', 'low']:
                if priority == '':
                    priority = 'medium'
                break
            else:
                print("Invalid priority. Please enter high, medium, or low.")

        # Get due date (optional)
        due_date = input("Enter due date (YYYY-MM-DD) [optional]: ").strip()
        if not due_date:
            due_date = None

        # Get category (optional)
        category = input("Enter category [optional]: ").strip()
        if not category:
            category = ""

        # Create new todo
        new_todo = Todo(
            id=self.next_id,
            task=task,
            priority=priority,
            due_date=due_date,
            category=category
        )

        self.todos.append(new_todo)
        self.next_id += 1

        print(f"Todo added successfully! (ID: {new_todo.id})")

    def view_todos(self):
        """Display all todos with statistics"""
        if not self.todos:
            print("\nNo todos found.")
            return

        print("\n======= YOUR TODOS =======")

        # Calculate statistics
        completed_count = sum(1 for todo in self.todos if todo.completed)
        total_count = len(self.todos)
        completion_percentage = 0
        if total_count > 0:
            completion_percentage = int((completed_count / total_count) * 100)

        print(f"Total: {total_count} | Completed: {completed_count} | Pending: {total_count - completed_count} | Completion: {completion_percentage}%")
        print("------------------------")

        for todo in self.todos:
            status = "[x]" if todo.completed else "[ ]"
            priority = f"[{todo.priority.upper()}]"
            category = f" [{todo.category}]" if todo.category else ""
            due_date = f" (Due: {todo.due_date})" if todo.due_date else ""
            print(f"{status} [{todo.id}] {todo.task} {priority}{category}{due_date}")

        print("========================")

    def mark_complete(self):
        """Toggle completion status of a todo"""
        if not self.todos:
            print("\nNo todos found.")
            return

        print("\n--- Mark Todo Complete/Incomplete ---")
        self.view_todos_for_action("mark")

        try:
            todo_id = int(input("Enter the ID of the todo to toggle (0 to cancel): "))
            if todo_id == 0:
                return
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        # Find the todo
        todo = None
        for t in self.todos:
            if t.id == todo_id:
                todo = t
                break

        if not todo:
            print("Todo not found!")
            return

        # Toggle completion status
        todo.completed = not todo.completed
        status = "completed" if todo.completed else "incomplete"
        print(f"Todo marked as {status}.")

    def delete_todo(self):
        """Delete a todo item"""
        if not self.todos:
            print("\nNo todos found.")
            return

        print("\n--- Delete Todo ---")
        self.view_todos_for_action("delete")

        try:
            todo_id = int(input("Enter the ID of the todo to delete (0 to cancel): "))
            if todo_id == 0:
                return
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        # Find and remove the todo
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                deleted_task = todo.task
                del self.todos[i]
                print(f"Todo '{deleted_task}' deleted successfully.")
                return

        print("Todo not found!")

    def view_todos_for_action(self, action):
        """Display todos for action (mark or delete)"""
        print(f"\n======= TODOS TO {action.upper()} =======")
        for todo in self.todos:
            status = "[x]" if todo.completed else "[ ]"
            priority = f"[{todo.priority.upper()}]"
            category = f" [{todo.category}]" if todo.category else ""
            due_date = f" (Due: {todo.due_date})" if todo.due_date else ""
            print(f"{status} [{todo.id}] {todo.task} {priority}{category}{due_date}")
        print("=====================================")

    def run(self):
        """Main application loop"""
        print("Welcome to the Console Todo App!")

        while self.running:
            self.show_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.add_todo()
            elif choice == '2':
                self.view_todos()
            elif choice == '3':
                self.mark_complete()
            elif choice == '4':
                self.delete_todo()
            elif choice == '5':
                print("Goodbye!")
                self.running = False

            # Pause to let user see results before showing menu again
            if choice in ['1', '3', '4']:
                input("\nPress Enter to continue...")


def main():
    """Main function to run the console todo app"""
    app = TodoConsoleApp()
    app.run()


if __name__ == "__main__":
    main()