# Meta - Employee Management System

A comprehensive Django-based Employee Management System that helps organizations manage their workforce efficiently.

## Features

- **Account Management**: User authentication and authorization
- **Admin Dashboard**: Administrative controls and oversight
- **Assignment Management**: Task and project assignments
- **Check-in System**: Employee attendance tracking
- **Leave Management**: Leave requests and approvals
- **Profile Management**: Employee profile handling

## Tech Stack

- Django (Python Web Framework)
- Static Files Management
- Media File Handling
- Environment Variables Support
- Vercel Deployment Ready

## Project Structure

```
Meta/
├── account/         # User authentication and account management
├── admins/          # Admin dashboard and controls
├── assign/          # Assignment management
├── checkin/         # Check-in system
├── home/            # Home page and main views
├── leave/           # Leave management system
├── profiles/        # User profile management
├── static/          # Static files (CSS, JS, Images)
├── media/          # User uploaded files
├── templates/       # HTML templates
└── manage.py       # Django management script
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file with necessary configurations

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment

The project is configured for Vercel deployment with `vercel.json` configuration file.

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and queries, please contact the development team.
