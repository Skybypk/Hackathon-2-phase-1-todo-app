# Flask Todo Web Application

A complete Flask-based Todo Web Application with modern UI, dark mode, drag and drop, and advanced features, integrated with the existing CLI todo app.

## Features

### Core Features
- Add, edit, delete, and mark todos as complete
- Due dates for tasks
- Priority levels (high, medium, low)
- Categories/tags for todos
- Progress tracking with completion percentage

### Bonus Features
- Dark/light mode toggle
- Drag and drop reordering
- Export todos to CSV
- Color-coded priorities
- Responsive design

### Data Persistence
- Uses the same `todos.json` file as the CLI app
- Both web and CLI can share data seamlessly

## Requirements

- Python 3.7+
- Flask 2.3.3

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the Application
Open your browser and go to: http://localhost:5000

## Project Structure

```
todo_web_app/
├── app.py                 # Main Flask application
├── todos.json             # Data persistence file (shared with CLI app)
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
└── static/
    ├── style.css          # CSS styling
    └── script.js          # JavaScript functionality
```

## API Endpoints

- `GET /` - Main page
- `POST /add` - Add a new todo
- `PUT /update/<id>` - Update a todo
- `DELETE /delete/<id>` - Delete a todo
- `PUT /toggle/<id>` - Toggle completion status
- `GET /export` - Export todos to CSV
- `GET /stats` - Get statistics

## Usage

### Adding Todos
- Enter your task in the input field
- Optionally set a due date, priority, and category
- Click "Add" button

### Managing Todos
- Check the checkbox to mark as complete
- Use the edit button (pencil icon) to modify
- Use the delete button (trash icon) to remove

### Filtering
- Use the filter buttons to show All, Active, or Completed todos

### Export
- Click "Export CSV" to download all todos as a CSV file

### Theme Toggle
- Click the moon/sun icon to switch between dark and light modes

## Integration with CLI App

The web application uses the same `todos.json` file as the CLI app, so todos created in either application will be visible in both.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with Flexbox/Grid
- **Icons**: Font Awesome
- **Data**: JSON file persistence

## Security Features

- Input validation
- Proper error handling
- Client-side and server-side validation

## Responsive Design

The application is fully responsive and works on mobile, tablet, and desktop devices.

## License

This project is part of a todo application development exercise.