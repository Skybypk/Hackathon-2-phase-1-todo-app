const readline = require('readline');

// Create readline interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// In-memory storage for todos
let todos = [];
let nextId = 1;

// Todo class to represent a todo item
class Todo {
    constructor(id, task, completed = false, createdAt = new Date().toISOString(), priority = "medium", category = "") {
        this.id = id;
        this.task = task;
        this.completed = completed;
        this.createdAt = createdAt;
        this.priority = priority; // high, medium, low
        this.category = category;
    }
}

// Helper function to clear the console (optional)
function clearConsole() {
    process.stdout.write('\x1Bc');
}

// Function to display the main menu
function showMenu() {
    console.log('\n======= TODO APP (Console Version) =======');
    console.log('1. Add Todo');
    console.log('2. View Todos');
    console.log('3. Mark Complete');
    console.log('4. Delete Todo');
    console.log('5. Exit');
    console.log('=========================================');
    promptForChoice();
}

// Function to prompt for user choice
function promptForChoice() {
    rl.question('Enter your choice (1-5): ', (choice) => {
        handleChoice(choice.trim());
    });
}

// Function to handle user choice
function handleChoice(choice) {
    switch (choice) {
        case '1':
            addTodo();
            break;
        case '2':
            viewTodos();
            break;
        case '3':
            markComplete();
            break;
        case '4':
            deleteTodo();
            break;
        case '5':
            console.log('Goodbye!');
            rl.close();
            break;
        default:
            console.log('Invalid choice. Please enter a number between 1 and 5.');
            showMenu();
            break;
    }
}

// Function to add a new todo
function addTodo() {
    rl.question('Enter the task: ', (task) => {
        task = task.trim();
        if (!task) {
            console.log('Task cannot be empty. Please try again.');
            showMenu();
            return;
        }

        // Ask for priority
        rl.question('Enter priority (high/medium/low) [default: medium]: ', (priority) => {
            priority = priority.trim().toLowerCase();
            if (!['high', 'medium', 'low'].includes(priority)) {
                priority = 'medium';
            }

            // Ask for category (optional)
            rl.question('Enter category (optional): ', (category) => {
                category = category.trim();

                const newTodo = new Todo(nextId++, task, false, new Date().toISOString(), priority, category);
                todos.push(newTodo);
                console.log(`Todo added successfully! (ID: ${newTodo.id})`);
                showMenu();
            });
        });
    });
}

// Function to view all todos
function viewTodos() {
    if (todos.length === 0) {
        console.log('\nNo todos found.');
        showMenu();
        return;
    }

    console.log('\n======= YOUR TODOS =======');

    // Calculate statistics
    const completedCount = todos.filter(todo => todo.completed).length;
    const totalCount = todos.length;
    const completionPercentage = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

    console.log(`Total: ${totalCount} | Completed: ${completedCount} | Pending: ${totalCount - completedCount} | Completion: ${completionPercentage}%`);
    console.log('------------------------');

    todos.forEach(todo => {
        const status = todo.completed ? '[x]' : '[ ]';
        const priority = `[${todo.priority.toUpperCase()}]`;
        const category = todo.category ? ` [${todo.category}]` : '';
        console.log(`${status} [${todo.id}] ${todo.task} ${priority}${category}`);
    });

    console.log('========================');
    showMenu();
}

// Function to mark a todo as complete/incomplete
function markComplete() {
    if (todos.length === 0) {
        console.log('\nNo todos found.');
        showMenu();
        return;
    }

    viewTodosForAction('mark complete');

    rl.question('Enter the ID of the todo to mark (or 0 to cancel): ', (idStr) => {
        const id = parseInt(idStr);

        if (id === 0) {
            showMenu();
            return;
        }

        const todoIndex = todos.findIndex(todo => todo.id === id);

        if (todoIndex === -1) {
            console.log('Todo not found. Please try again.');
            showMenu();
            return;
        }

        // Toggle completion status
        todos[todoIndex].completed = !todos[todoIndex].completed;
        const status = todos[todoIndex].completed ? 'completed' : 'incomplete';
        console.log(`Todo marked as ${status}.`);
        showMenu();
    });
}

// Function to delete a todo
function deleteTodo() {
    if (todos.length === 0) {
        console.log('\nNo todos found.');
        showMenu();
        return;
    }

    viewTodosForAction('delete');

    rl.question('Enter the ID of the todo to delete (or 0 to cancel): ', (idStr) => {
        const id = parseInt(idStr);

        if (id === 0) {
            showMenu();
            return;
        }

        const todoIndex = todos.findIndex(todo => todo.id === id);

        if (todoIndex === -1) {
            console.log('Todo not found. Please try again.');
            showMenu();
            return;
        }

        const deletedTodo = todos.splice(todoIndex, 1)[0];
        console.log(`Todo "${deletedTodo.task}" deleted successfully.`);
        showMenu();
    });
}

// Helper function to view todos for action (mark complete or delete)
function viewTodosForAction(action) {
    console.log(`\n======= TODOS TO ${action.toUpperCase()} =======`);
    todos.forEach(todo => {
        const status = todo.completed ? '[x]' : '[ ]';
        const priority = `[${todo.priority.toUpperCase()}]`;
        const category = todo.category ? ` [${todo.category}]` : '';
        console.log(`${status} [${todo.id}] ${todo.task} ${priority}${category}`);
    });
    console.log('=====================================');
}

// Start the application
function startApp() {
    console.log('Welcome to the Console Todo App!');
    showMenu();
}

// Handle exit gracefully
rl.on('close', () => {
    console.log('\nThank you for using the Console Todo App!');
    process.exit(0);
});

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
    console.log('\n\nGoodbye!');
    rl.close();
});

// Start the application
startApp();