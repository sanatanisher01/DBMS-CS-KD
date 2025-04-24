# SportSphere - Sports Facility Management System

SportSphere is a comprehensive web application for managing sports facilities, bookings, equipment, and maintenance. It provides different functionality for students/faculty, sports staff, and administrators.

## Features

- **User Management**: Different roles (Student/Faculty, Staff, Admin) with appropriate permissions
- **Facility Management**: Add, edit, and view sports facilities
- **Booking System**: Book facilities, check availability, and manage bookings
- **Equipment Inventory**: Track equipment associated with facilities
- **Maintenance Reporting**: Report and track maintenance issues
- **Analytics Dashboard**: View usage statistics and reports

## User Roles

1. **Student/Faculty**
   - Book facilities and view schedule
   - Cancel or reschedule usage
   - Report damaged equipment

2. **Sports Staff**
   - Approve/deny slot requests
   - Maintain usage records
   - Manage equipment inventory

3. **Admin**
   - Configure booking rules
   - Analyze facility usage
   - Manage staff accounts and facility status

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: MySQL

## Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sportsphere.git
   cd sportsphere
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a MySQL database named `sportsphere`
   - Update the database credentials in `sportsphere/settings.py` if needed (default: username=root, password=Shiva)

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Initialize sample data:
   ```
   python init_data.py
   ```

7. Run the development server:
   ```
   python run.py
   ```

8. Access the application at http://127.0.0.1:8000/

## Default User Accounts

The following user accounts are created when you run `init_data.py`:

1. **Admin User**
   - Username: admin
   - Password: admin123

2. **Staff User**
   - Username: staff
   - Password: staff123

3. **Faculty User**
   - Username: faculty
   - Password: faculty123

4. **Student User**
   - Username: student
   - Password: student123

## License

This project is licensed under the MIT License - see the LICENSE file for details.
