#!/usr/bin/env python3
"""
A simple command-line todo application using Python.
Phase 1 implementation following Spec-Driven Development principles.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional


class TodoApp:
    """Main Todo application class managing all todo operations."""

    def __init__(self, data_file: str = "todos.json"):
        """
        Initialize the TodoApp with a data file.

        Args:
            data_file: Path to the JSON file for data persistence
        """
        self.data_file = data_file
        self.todos = self.load_todos()

    def load_todos(self) -> List[Dict]:
        """
        Load todos from a JSON file.

        Returns:
            List of todo dictionaries
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure data is a list
                    if not isinstance(data, list):
                        print(f"Warning: {self.data_file} does not contain a list. Resetting.")
                        return []
                    return data
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.data_file}. Resetting.")
            return []
        except Exception as e:
            print(f"Error reading {self.data_file}: {e}")
            return []

    def save_todos(self) -> bool:
        """
        Save todos to a JSON file.

        Returns:
            True if save was successful, False otherwise
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving to {self.data_file}: {e}")
            return False

    def add_todo(self, task: str) -> bool:
        """
        Add a new todo.

        Args:
            task: The task description to add

        Returns:
            True if todo was added successfully, False otherwise
        """
        if not task or not task.strip():
            print("Error: Task description cannot be empty.")
            return False

        # Generate unique ID (using max ID + 1 to handle deletions properly)
        if self.todos:
            next_id = max(todo["id"] for todo in self.todos) + 1
        else:
            next_id = 1

        todo = {
            "id": next_id,
            "task": task.strip(),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.todos.append(todo)

        if self.save_todos():
            try:
                print(f"Added task: {task}")
            except UnicodeEncodeError:
                # Handle case where terminal can't display certain Unicode characters
                print(f"Added task: [ID {self.todos[-1]['id']}] (content contains special characters)")
            return True
        else:
            print("Error: Failed to save todo to file.")
            # Remove the todo if save failed
            self.todos.remove(todo)
            return False

    def list_todos(self) -> None:
        """List all todos with their status."""
        if not self.todos:
            print("No todos found!")
            return

        print("\nYour todos:")
        # Sort by ID to maintain consistent order
        sorted_todos = sorted(self.todos, key=lambda x: x["id"])
        for todo in sorted_todos:
            status = "X" if todo["completed"] else "O"
            try:
                print(f"{todo['id']}. [{status}] {todo['task']}")
            except UnicodeEncodeError:
                # Handle case where terminal can't display certain Unicode characters
                print(f"{todo['id']}. [{status}] [Task contains special characters]")

    def complete_todo(self, todo_id: str) -> bool:
        """
        Mark a todo as completed.

        Args:
            todo_id: The ID of the todo to complete

        Returns:
            True if todo was completed successfully, False otherwise
        """
        try:
            todo_id_int = int(todo_id)
        except ValueError:
            print(f"Error: '{todo_id}' is not a valid todo ID.")
            return False

        for todo in self.todos:
            if todo["id"] == todo_id_int:
                if todo["completed"]:
                    try:
                        print(f"Task is already completed: {todo['task']}")
                    except UnicodeEncodeError:
                        print(f"Task is already completed: [ID {todo['id']}] (content contains special characters)")
                else:
                    todo["completed"] = True
                    if self.save_todos():
                        try:
                            print(f"Completed task: {todo['task']}")
                        except UnicodeEncodeError:
                            print(f"Completed task: [ID {todo['id']}] (content contains special characters)")
                        return True
                    else:
                        print("Error: Failed to save changes to file.")
                        # Revert the change if save failed
                        todo["completed"] = False
                        return False
                return True

        print(f"Todo with ID {todo_id} not found!")
        return False

    def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if todo was deleted successfully, False otherwise
        """
        try:
            todo_id_int = int(todo_id)
        except ValueError:
            print(f"Error: '{todo_id}' is not a valid todo ID.")
            return False

        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id_int:
                deleted_task = todo["task"]
                del self.todos[i]
                if self.save_todos():
                    try:
                        print(f"Deleted task: {deleted_task}")
                    except UnicodeEncodeError:
                        print(f"Deleted task: [ID {todo_id_int}] (content contains special characters)")
                    return True
                else:
                    print("Error: Failed to save changes to file.")
                    # Revert the deletion if save failed
                    self.todos.insert(i, todo)
                    return False

        print(f"Todo with ID {todo_id} not found!")
        return False


def show_usage() -> None:
    """Display usage information for the todo app."""
    print("Usage: python todo.py [add|list|complete|delete] [task/id]")
    print("  add 'task'     - Add a new todo")
    print("  list           - List all todos")
    print("  complete ID    - Mark a todo as completed")
    print("  delete ID      - Delete a todo")
    print("  help           - Show this help message")


def main():
    """Main entry point for the todo application."""
    app = TodoApp()

    if len(sys.argv) < 2:
        show_usage()
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task to add.")
            print("Usage: python todo.py add 'task description'")
            return
        task = " ".join(sys.argv[2:])
        app.add_todo(task)
    elif command == "list":
        app.list_todos()
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: Please provide a todo ID to complete.")
            print("Usage: python todo.py complete ID")
            return
        app.complete_todo(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a todo ID to delete.")
            print("Usage: python todo.py delete ID")
            return
        app.delete_todo(sys.argv[2])
    elif command == "help":
        show_usage()
    else:
        print(f"Error: Unknown command: {command}")
        show_usage()


if __name__ == "__main__":
    main()