# Event Management System

A Django-based Event Management System that allows users to create, manage, and register for events with email notifications.

## Features

### 1. User Authentication
- Register, Log In, and Log Out
- Two types of users:
  - **Event Organizers**: Can create and manage events
  - **Participants**: Can register and deregister from events

### 2. Event Management
- **Event Organizers** can:
  - Create, Read, Update, and Delete events

### 3. Event Registration
- **Participants** can:
  - Register and deregister from events

### 4. Notifications & Emails
- **Event Organizers** receive a confirmation email upon event creation
- **Participants** receive a confirmation email upon event registration
- Participants get notified when event details are updated or deleted
- Organizers get notified when an event reaches full capacity
- In-app notifications

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/Hemil08/Event-Management-System.git
   cd Event-Management-System
   ```

2. **Create and Activate Virtual Environment**
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```sh
   python manage.py migrate
   ```

5. **Run the Server**
   ```sh
   python manage.py runserver
   ```

## Usage
- Register and log in as an **Event Organizer** to create and manage events.
- Register and log in as a **Participant** to sign up for events.

## Contributing
Feel free to submit pull requests or open issues to improve the project.
