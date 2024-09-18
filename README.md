# Task Management System

#### Video Demo:  <https://youtu.be/CoVKNr2L0R4?si=0r9Z90u-VmC5HuKw>

#### Description:

This task management system is a Python-based command-line application designed to help users organize and manage their tasks efficiently. The system offers a range of features to enhance productivity and ensure that users stay on top of their responsibilities.

Key Features:
1. **Add Tasks**: Users can add new tasks with detailed information including task name, due date, category, priority, recurrence, and additional notes. This ensures that users can capture all relevant information about their tasks.

2. **View Tasks**: The system allows users to view their pending tasks, sorted by priority and due date. This feature helps users focus on the most important and urgent tasks first.

3. **Mark Tasks as Complete**: Users can mark tasks as completed when they finish them. For recurring tasks, the system automatically creates a new instance of the task for the next due date.

4. **View Task History**: This feature enables users to review their completed tasks, and remind themselves of what they have accomplished.

5. **Delete Tasks**: Users can remove tasks from the system if they are no longer relevant or needed.

6. **Recurring Tasks**: The system supports the creation of recurring tasks (daily, weekly, or monthly), automating the process of task repetition and reducing manual data entry.

7. **Notification System**: A key feature of this project is the notification system. It runs in a separate process and checks for upcoming tasks every minute. It sends desktop notifications for tasks due within the next 30 minutes. Notifications are sent every 5 minutes and when the task is due under 5 minutes, notifications are sent every minute. This helps create the urgency of due tasks.

Technical Implementation:
The project is implemented in Python and makes use of several libraries to enhance its functionality:

- `json`: Used for storing and retrieving task data in a JSON file, allowing for data persistence between sessions.
- `datetime`: Employed for handling dates and times, crucial for managing task due dates and calculating time remaining.
- `plyer`: Utilized to send desktop notifications, enhancing the user experience with timely reminders.
- `schedule`: Used to run the notification checks at regular intervals.
- `multiprocessing`: Implemented to run the notification system in a separate process, ensuring that it doesn't interfere with the main application loop.

The main application loop provides a simple text-based interface where users can choose from various options to interact with their tasks. The system continuously runs until the user chooses to exit, at which point it ensures that the notification system is properly shut down.

Data Storage:
Tasks are stored in a JSON file (`tasks.json`), which allows for easy data persistence and retrieval. Each task is represented as a dictionary containing all relevant information, making it simple to add new attributes to tasks in future iterations of the project.

Testing:
The project includes a test suite (`test_project.py`) that ensures the core features of the application work as expected.

Future Enhancements:
While the current implementation provides a solid foundation for task management, there are several areas where the project could be expanded in the future:

1. Graphical User Interface (GUI): Implementing a GUI would make the application more user-friendly and accessible to a broader audience.
2. Database Integration: Moving from file-based storage to a database system would improve data management and allow for more complex querying and reporting features.
3. User Authentication: Adding user accounts would enable multi-user support, making the application suitable for team environments.
4. Integration with External Calendars: Allowing synchronization with popular calendar applications would enhance the system's utility in a user's broader productivity ecosystem.
5. Advanced Filtering and Sorting: Implementing more sophisticated task filtering and sorting options would help users manage larger numbers of tasks more effectively.

In conclusion, this task management showcases the use of functions, file I/O, data structures, external libraries, and multiprocessing to create a practical and useful application. This project is the basic upon finishing the CS50P course, and future learning should allow me to bring this app to another level.