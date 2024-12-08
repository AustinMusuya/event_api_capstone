## Setup Instructions

### Prerequisites

1. **Python 3.8+**  
   Make sure Python 3.8 or later is installed on your machine.

2. **PostgreSQL** (For production deployment)  
   You can install PostgreSQL locally or use an external service.

3. **Virtual Environment (Recommended)**  
   Use a virtual environment to manage dependencies and keep your project isolated from other Python projects.

---

### Steps to Set Up the Project

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/event-management-api.git
   cd event-management-api

2. **Create a Virtual Environment**

   Create & activate a Virtual Environment

   ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate

3. **Install Dependancies**

   Install the required Python packages:

   ```bash
    pip install -r requirements.txt

4. **Configure the Database**

   Set up your MySQL database (or SQLite for development). Update the DATABASES configuration in event_project/settings.py with the correct credentials.

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'event_db',
        'USER': 'your-username',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
        }
    }


5. **Apply Migrations**

   Run the migrations to set up the database schema:

   ```bash
    python manage.py migrate


6. **Create a Superuser (Admin)**

   Create a superuser to manage the app via Django admin:

   ```bash
    python manage.py createsuperuser


7. **Run the Development Server**

   Start the Django development server to test the API:

   ```bash
    python manage.py runserver

    The API should now be running at http://127.0.0.1:8000/.

8. **Testing the API**

    To test the API, use tools like Postman or CURL, or navigate to the API endpoints. For example:

    GET /api/events/ - List all events
    POST /api/users/ - Register a new user
    POST /api/users/login/ - Log in to the API (using token-based authentication)
    POST /api/events/ - Create a new event
               
   
 
