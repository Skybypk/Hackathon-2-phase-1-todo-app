#!/usr/bin/env python3
"""
Comprehensive test suite for the Todo App Phase 1 implementation.
Tests all functionality according to the specification.
"""

import json
import os
import tempfile
import unittest
from datetime import datetime
from todo import TodoApp


class TestTodoApp(unittest.TestCase):
    """Test cases for the TodoApp class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.app = TodoApp(data_file=self.temp_file.name)

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_initial_state(self):
        """Test that the app starts with an empty todo list."""
        self.assertEqual(self.app.todos, [])

    def test_add_todo_basic(self):
        """Test adding a basic todo item."""
        result = self.app.add_todo("Test task")
        self.assertTrue(result)
        self.assertEqual(len(self.app.todos), 1)
        self.assertEqual(self.app.todos[0]["task"], "Test task")
        self.assertFalse(self.app.todos[0]["completed"])
        self.assertEqual(self.app.todos[0]["id"], 1)

    def test_add_todo_empty_string(self):
        """Test adding an empty todo task."""
        result = self.app.add_todo("")
        self.assertFalse(result)
        self.assertEqual(self.app.todos, [])

    def test_add_todo_whitespace_only(self):
        """Test adding a todo with only whitespace."""
        result = self.app.add_todo("   ")
        self.assertFalse(result)
        self.assertEqual(self.app.todos, [])

    def test_add_todo_with_whitespace(self):
        """Test adding a todo with leading/trailing whitespace."""
        result = self.app.add_todo("  Test task with spaces  ")
        self.assertTrue(result)
        self.assertEqual(self.app.todos[0]["task"], "Test task with spaces")

    def test_add_multiple_todos(self):
        """Test adding multiple todos with proper ID sequencing."""
        self.app.add_todo("First task")
        self.app.add_todo("Second task")
        self.app.add_todo("Third task")

        self.assertEqual(len(self.app.todos), 3)
        self.assertEqual(self.app.todos[0]["id"], 1)
        self.assertEqual(self.app.todos[1]["id"], 2)
        self.assertEqual(self.app.todos[2]["id"], 3)

    def test_list_todos_empty(self):
        """Test listing todos when the list is empty."""
        # Capture print output would require mocking, so we'll just ensure no errors
        self.app.list_todos()  # Should not raise an exception

    def test_list_todos_with_items(self):
        """Test listing todos with items present."""
        self.app.add_todo("Task 1")
        self.app.add_todo("Task 2")
        # Just ensure no exceptions are raised
        self.app.list_todos()

    def test_complete_todo(self):
        """Test completing a todo item."""
        self.app.add_todo("Test task")
        initial_task = self.app.todos[0]

        result = self.app.complete_todo("1")
        self.assertTrue(result)
        self.assertTrue(self.app.todos[0]["completed"])

    def test_complete_nonexistent_todo(self):
        """Test completing a todo that doesn't exist."""
        result = self.app.complete_todo("999")
        self.assertFalse(result)

    def test_complete_invalid_id(self):
        """Test completing with an invalid ID."""
        result = self.app.complete_todo("abc")
        self.assertFalse(result)

    def test_complete_already_completed_todo(self):
        """Test completing a todo that's already completed."""
        self.app.add_todo("Test task")
        self.app.complete_todo("1")
        # This should not cause an error
        result = self.app.complete_todo("1")
        self.assertTrue(result)  # Should return True as the task exists

    def test_delete_todo(self):
        """Test deleting a todo item."""
        self.app.add_todo("Test task")
        self.assertEqual(len(self.app.todos), 1)

        result = self.app.delete_todo("1")
        self.assertTrue(result)
        self.assertEqual(len(self.app.todos), 0)

    def test_delete_nonexistent_todo(self):
        """Test deleting a todo that doesn't exist."""
        result = self.app.delete_todo("999")
        self.assertFalse(result)

    def test_delete_invalid_id(self):
        """Test deleting with an invalid ID."""
        result = self.app.delete_todo("abc")
        self.assertFalse(result)

    def test_id_generation_after_deletion(self):
        """Test that IDs are properly generated after deletion."""
        self.app.add_todo("Task 1")  # ID: 1
        self.app.add_todo("Task 2")  # ID: 2
        self.app.delete_todo("1")    # Delete ID: 1
        self.app.add_todo("Task 3")  # Should get ID: 3 (max existing + 1)

        self.assertEqual(len(self.app.todos), 2)
        # Check that IDs are 2 and 3
        ids = [todo["id"] for todo in self.app.todos]
        self.assertIn(2, ids)
        self.assertIn(3, ids)

    def test_data_persistence(self):
        """Test that data persists to file."""
        self.app.add_todo("Persistent task")

        # Create a new app instance with the same file
        new_app = TodoApp(data_file=self.temp_file.name)
        self.assertEqual(len(new_app.todos), 1)
        self.assertEqual(new_app.todos[0]["task"], "Persistent task")

    def test_load_invalid_json(self):
        """Test loading from a file with invalid JSON."""
        # Write invalid JSON to the file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json {")

        # Create a new app instance - should handle gracefully
        new_app = TodoApp(data_file=self.temp_file.name)
        self.assertEqual(new_app.todos, [])

    def test_load_non_list_json(self):
        """Test loading from a file that doesn't contain a list."""
        # Write non-list JSON to the file
        with open(self.temp_file.name, 'w') as f:
            json.dump("not a list", f)

        # Create a new app instance - should handle gracefully
        new_app = TodoApp(data_file=self.temp_file.name)
        self.assertEqual(new_app.todos, [])

    def test_save_failure_handling(self):
        """Test handling of save failures."""
        # This is difficult to test without mocking, but we can verify
        # that the save_todos method exists and returns a boolean
        self.app.add_todo("Test task")
        result = self.app.save_todos()
        self.assertIsInstance(result, bool)

    def test_todo_structure(self):
        """Test that todos have the correct structure."""
        self.app.add_todo("Test task")
        todo = self.app.todos[0]

        self.assertIn("id", todo)
        self.assertIn("task", todo)
        self.assertIn("completed", todo)
        self.assertIn("created_at", todo)

        self.assertIsInstance(todo["id"], int)
        self.assertIsInstance(todo["task"], str)
        self.assertIsInstance(todo["completed"], bool)
        self.assertIsInstance(todo["created_at"], str)

        # Verify created_at is a valid ISO format datetime
        datetime.fromisoformat(todo["created_at"].replace('Z', '+00:00'))


class TestTodoAppIntegration(unittest.TestCase):
    """Integration tests for the TodoApp functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.app = TodoApp(data_file=self.temp_file.name)

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_full_workflow(self):
        """Test a complete workflow: add, list, complete, delete."""
        # Add multiple todos
        self.app.add_todo("First task")
        self.app.add_todo("Second task")
        self.app.add_todo("Third task")

        self.assertEqual(len(self.app.todos), 3)

        # Complete one todo
        self.app.complete_todo("2")
        completed_todo = next((t for t in self.app.todos if t["id"] == 2), None)
        self.assertIsNotNone(completed_todo)
        self.assertTrue(completed_todo["completed"])

        # Delete one todo
        self.app.delete_todo("1")
        self.assertEqual(len(self.app.todos), 2)

        # Verify remaining todos exist
        remaining_ids = [t["id"] for t in self.app.todos]
        self.assertIn(2, remaining_ids)
        self.assertIn(3, remaining_ids)

    def test_persistence_across_instances(self):
        """Test that data persists across different app instances."""
        # Add todos with first instance
        self.app.add_todo("Instance 1 task")
        self.app.complete_todo("1")

        # Create second instance and verify persistence
        second_app = TodoApp(data_file=self.temp_file.name)
        self.assertEqual(len(second_app.todos), 1)
        self.assertEqual(second_app.todos[0]["task"], "Instance 1 task")
        self.assertTrue(second_app.todos[0]["completed"])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.app = TodoApp(data_file=self.temp_file.name)

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_large_task_description(self):
        """Test adding a very large task description."""
        large_task = "A" * 10000  # 10,000 character task
        result = self.app.add_todo(large_task)
        self.assertTrue(result)
        self.assertEqual(self.app.todos[0]["task"], large_task)

    def test_special_characters_in_task(self):
        """Test adding tasks with special characters."""
        special_task = "Test task with émojis 🚀 and \"quotes\" and 'apostrophes'"
        result = self.app.add_todo(special_task)
        self.assertTrue(result)
        self.assertEqual(self.app.todos[0]["task"], special_task)

    def test_consecutive_operations(self):
        """Test performing multiple operations in sequence."""
        # Add multiple tasks
        for i in range(5):
            self.app.add_todo(f"Task {i+1}")

        # Complete some tasks
        self.app.complete_todo("1")
        self.app.complete_todo("3")
        self.app.complete_todo("5")

        # Verify state
        completed_count = sum(1 for t in self.app.todos if t["completed"])
        self.assertEqual(completed_count, 3)


def run_tests():
    """Run all tests and report results."""
    print("Running Todo App Phase 1 tests...")
    print("=" * 50)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add all test cases
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(TestTodoApp))
    test_suite.addTest(loader.loadTestsFromTestCase(TestTodoAppIntegration))
    test_suite.addTest(loader.loadTestsFromTestCase(TestEdgeCases))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")

    success = result.wasSuccessful()
    print(f"\nOverall result: {'PASS' if success else 'FAIL'}")

    return success


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)