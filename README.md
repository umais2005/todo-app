# Todo App with SQLite and Tkinter

This project is a simple **To-Do List application** built using Python, Tkinter for the graphical user interface, and SQLite for the database. The application allows users to add, display, update, and delete tasks with a priority level, description, category, and date.

## Features

- **Task Management**: Add, display, and delete tasks.
- **Task Sorting**: Sort tasks by category, description, or priority.
- **Category Management**: Assign tasks to categories and color-code them.
- **Data Persistence**: Uses SQLite to store tasks and categories persistently.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/todo-app.git
    ```
2. **Navigate to the project directory**:
    ```sh
    cd todo-app
    ```
3. **Install the required packages** (if not already installed):
    ```sh
    pip install tk
    ```

## Usage

1. **Run the application**:
    ```sh
    python todo_app.py
    ```
2. **Add a new task**: 
   - Click the "Add" button to input a task's priority, description, and category.
   - Confirm or cancel the task creation.
3. **View tasks**: 
   - Tasks are displayed with their priority, description, category, and the date they were added.
   - Use the "SortBy" dropdown to sort tasks by category, description, or priority.
4. **Delete a task**:
   - Click the "Delete" button next to a task to remove it from the list.
   
## Code Overview

- **generate_color()**: Generates a random color for new task categories.
- **Taskitem Class**: Custom label widget that displays task details, including background color based on category.
- **GUI Class**: Main class for handling the application interface and interactions.
  - **show_tasks()**: Fetches and displays tasks from the database.
  - **show_input()**: Shows the input fields for adding a new task.
  - **refresh()**: Refreshes the task list after adding a new task.
  - **destroy_input()**: Clears the input fields.
  - **delete_task()**: Deletes a task from the database.
  - **add_record()**: Validates and adds a new task to the database.
  - **add_category()**: Adds a new category to the database with a unique color.
- **Database Setup**: 
  - **tasks** table: Stores task details (priority, description, category, date).
  - **categories** table: Stores categories and their associated colors.

## Dependencies

- **Python 3.x**
- **Tkinter**: For creating the graphical user interface.
- **SQLite3**: For database management.

## Future Enhancements

- Add the ability to update tasks.
- Implement task reminders or notifications.
- Improve the user interface with more advanced features like task filtering.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was inspired by the need for a simple, lightweight to-do list application with category-based color coding.
