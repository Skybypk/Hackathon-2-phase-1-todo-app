// Theme management
function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.setAttribute('data-theme', themeName);
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'dark') {
        setTheme('light');
    } else {
        setTheme('dark');
    }
}

// Initialize theme
if (localStorage.getItem('theme') === 'dark') {
    setTheme('dark');
} else {
    setTheme('light');
}

// DOM elements
const themeToggle = document.getElementById('theme-toggle');
const addForm = document.getElementById('add-form');
const taskInput = document.getElementById('task-input');
const dueDateInput = document.getElementById('due-date-input');
const priorityInput = document.getElementById('priority-input');
const categoryInput = document.getElementById('category-input');
const todosList = document.getElementById('todos-list');
const filterBtns = document.querySelectorAll('.filter-btn');
const exportBtn = document.getElementById('export-btn');
const modal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-form');
const editId = document.getElementById('edit-id');
const editTask = document.getElementById('edit-task');
const editDueDate = document.getElementById('edit-due-date');
const editPriority = document.getElementById('edit-priority');
const editCategory = document.getElementById('edit-category');

// Current filter state
let currentFilter = 'all';

// Theme toggle event
themeToggle.addEventListener('click', toggleTheme);

// Add todo form submission
addForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const task = taskInput.value.trim();
    const dueDate = dueDateInput.value;
    const priority = priorityInput.value;
    const category = categoryInput.value.trim();

    if (!task) {
        alert('Please enter a task');
        return;
    }

    try {
        const response = await fetch('/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: task,
                due_date: dueDate || null,
                priority: priority,
                category: category
            })
        });

        const result = await response.json();

        if (result.success) {
            // Reset form
            taskInput.value = '';
            dueDateInput.value = '';
            priorityInput.value = 'medium';
            categoryInput.value = '';

            // Refresh the page to show the new todo
            location.reload();
        } else {
            alert('Error adding todo: ' + result.error);
        }
    } catch (error) {
        alert('Error adding todo: ' + error.message);
    }
});

// Filter todos
filterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        // Update active button
        filterBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        // Set current filter
        currentFilter = this.dataset.filter;

        // Filter todos
        filterTodos();
    });
});

function filterTodos() {
    const todos = document.querySelectorAll('.todo-item');

    todos.forEach(todo => {
        const isCompleted = todo.classList.contains('completed');

        switch(currentFilter) {
            case 'active':
                todo.style.display = isCompleted ? 'none' : 'block';
                break;
            case 'completed':
                todo.style.display = isCompleted ? 'block' : 'none';
                break;
            case 'all':
            default:
                todo.style.display = 'block';
                break;
        }
    });
}

// Export button
exportBtn.addEventListener('click', function() {
    window.location.href = '/export';
});

// Todo checkbox toggle
document.addEventListener('change', async function(e) {
    if (e.target.classList.contains('todo-checkbox-input')) {
        const todoItem = e.target.closest('.todo-item');
        const todoId = parseInt(todoItem.dataset.id);

        try {
            const response = await fetch(`/toggle/${todoId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (result.success) {
                // Update UI
                todoItem.classList.toggle('completed');
                const todoText = todoItem.querySelector('.todo-text');
                todoText.classList.toggle('completed-text');

                // Update priority indicator
                const priorityIndicator = todoItem.querySelector('.todo-priority');
                const priority = result.todo.priority;
                priorityIndicator.className = `todo-priority priority-${priority}`;

                // Update progress bar
                if (result.completion_percentage !== undefined) {
                    const progressFill = document.querySelector('.progress-fill');
                    const progressLabel = document.querySelector('.progress-label');

                    progressFill.style.width = result.completion_percentage + '%';
                    progressLabel.textContent = `Completion: ${result.completion_percentage}%`;

                    // Update stats
                    updateStats();
                }
            } else {
                alert('Error updating todo: ' + result.error);
                // Revert the checkbox state
                e.target.checked = !e.target.checked;
            }
        } catch (error) {
            alert('Error updating todo: ' + error.message);
            // Revert the checkbox state
            e.target.checked = !e.target.checked;
        }
    }
});

// Delete todo
document.addEventListener('click', async function(e) {
    if (e.target.closest('.btn-delete')) {
        const todoItem = e.target.closest('.todo-item');
        const todoId = parseInt(todoItem.dataset.id);

        if (confirm('Are you sure you want to delete this todo?')) {
            try {
                const response = await fetch(`/delete/${todoId}`, {
                    method: 'DELETE'
                });

                const result = await response.json();

                if (result.success) {
                    // Animate removal and then remove from DOM
                    todoItem.style.animation = 'fadeOut 0.3s ease';
                    setTimeout(() => {
                        todoItem.remove();
                        updateStats();
                    }, 300);
                } else {
                    alert('Error deleting todo: ' + result.error);
                }
            } catch (error) {
                alert('Error deleting todo: ' + error.message);
            }
        }
    }
});

// Edit todo - open modal
document.addEventListener('click', function(e) {
    if (e.target.closest('.btn-edit')) {
        const todoItem = e.target.closest('.todo-item');
        const todoId = parseInt(todoItem.dataset.id);

        // Get todo data
        const todoText = todoItem.querySelector('.todo-text').textContent;
        const dueDate = todoItem.querySelector('.todo-due-date');
        const priority = todoItem.dataset.priority;
        const category = todoItem.dataset.category;

        // Fill modal form
        editId.value = todoId;
        editTask.value = todoText;
        editDueDate.value = dueDate ? dueDate.textContent.split(' ')[1] : '';
        editPriority.value = priority;
        editCategory.value = category;

        // Show modal
        modal.style.display = 'block';
    }
});

// Edit form submission
editForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const todoId = parseInt(editId.value);
    const task = editTask.value.trim();
    const dueDate = editDueDate.value;
    const priority = editPriority.value;
    const category = editCategory.value.trim();

    if (!task) {
        alert('Please enter a task');
        return;
    }

    try {
        const response = await fetch(`/update/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: task,
                due_date: dueDate || null,
                priority: priority,
                category: category
            })
        });

        const result = await response.json();

        if (result.success) {
            // Close modal
            modal.style.display = 'none';

            // Refresh the page to show updated todo
            location.reload();
        } else {
            alert('Error updating todo: ' + result.error);
        }
    } catch (error) {
        alert('Error updating todo: ' + error.message);
    }
});

// Close modal when clicking X
document.querySelector('.close').addEventListener('click', function() {
    modal.style.display = 'none';
});

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Cancel edit button
document.querySelector('.cancel-edit').addEventListener('click', function() {
    modal.style.display = 'none';
});

// Update stats function
async function updateStats() {
    try {
        const response = await fetch('/stats');
        const stats = await response.json();

        if (stats) {
            // Update stats display
            const statItems = document.querySelectorAll('.stat-item');
            statItems[0].textContent = `Total: ${stats.total}`;
            statItems[1].textContent = `Completed: ${stats.completed}`;
            statItems[2].textContent = `Pending: ${stats.total - stats.completed}`;
        }
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Drag and drop functionality
let draggedItem = null;

document.addEventListener('dragstart', function(e) {
    if (e.target.classList.contains('todo-item')) {
        draggedItem = e.target;
        e.target.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', e.target.outerHTML);
    }
});

document.addEventListener('dragend', function(e) {
    if (e.target.classList.contains('todo-item')) {
        e.target.classList.remove('dragging');
        draggedItem = null;
    }
});

document.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
});

document.addEventListener('dragenter', function(e) {
    if (e.target.classList.contains('todo-item')) {
        e.target.classList.add('drag-over');
    }
});

document.addEventListener('dragleave', function(e) {
    if (e.target.classList.contains('todo-item')) {
        e.target.classList.remove('drag-over');
    }
});

document.addEventListener('drop', async function(e) {
    e.preventDefault();

    if (e.target.classList.contains('todo-item') && draggedItem !== e.target) {
        e.target.classList.remove('drag-over');

        // Swap positions in the UI
        const todosContainer = todosList;
        const todos = Array.from(todosContainer.children);
        const draggedIndex = todos.indexOf(draggedItem);
        const targetIndex = todos.indexOf(e.target);

        if (draggedIndex < targetIndex) {
            todosContainer.insertBefore(draggedItem, e.target.nextSibling);
        } else {
            todosContainer.insertBefore(draggedItem, e.target);
        }

        // In a real app, you would update the order on the server
        // For this implementation, we'll just show a message
        console.log('Todo reordering would be saved to server in a real implementation');
    }
});

// Add drag attribute to todo items for better UX
document.querySelectorAll('.todo-item').forEach(item => {
    item.setAttribute('draggable', 'true');
});

// Initialize filters
filterTodos();

// Add hash function for category colors (since we can't use Jinja2 in JS)
String.prototype.hashCode = function() {
    let hash = 0;
    for (let i = 0; i < this.length; i++) {
        const char = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash);
};

// Apply drag and drop styles
document.querySelectorAll('.todo-item').forEach(item => {
    item.setAttribute('draggable', 'true');
});

// Assign colors to categories
document.querySelectorAll('.todo-category').forEach(categorySpan => {
    const category = categorySpan.getAttribute('data-category');
    const hue = Math.abs(category.hashCode()) % 360;
    categorySpan.style.backgroundColor = `hsl(${hue}, 70%, 85%)`;
    categorySpan.style.color = `hsl(${hue}, 70%, 30%)`;
});

// Add hash function for category colors
String.prototype.hashCode = function() {
    let hash = 0;
    for (let i = 0; i < this.length; i++) {
        const char = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash);
};