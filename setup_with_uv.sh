#!/bin/bash
# Script to demonstrate using the todo app with uv

echo "Setting up todo app with uv..."

# Create virtual environment
echo "Creating virtual environment..."
uv venv

# Activate virtual environment and install the package
echo "Installing todo app in development mode..."
source .venv/Scripts/activate && uv pip install -e .

echo ""
echo "Todo app installed successfully!"
echo ""
echo "Usage examples:"
echo "  Add a todo: python todo.py add \"My new task\""
echo "  List todos: python todo.py list"
echo "  Complete todo: python todo.py complete 1"
echo "  Delete todo: python todo.py delete 1"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source .venv/Scripts/activate"
echo ""