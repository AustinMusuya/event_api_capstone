## Setup Instructions

### Prerequisites

1. **Python 3.8+**  
   Make sure Python 3.8 or later is installed on your machine.

2. **MySQL** (For production deployment)  
   You can install MySQL locally or use an external service.

3. **Git**: Recommended for version control. 
   You can install from the official git website

4. **Virtual Environment (Recommended)**  
   Use a virtual environment to manage dependencies and keep your project isolated from other Python projects.

---

### Steps to Set Up the Project

1. **Clone the Repository**

What does this mean?
You’re copying the project from an online location (GitHub) to your computer so you can work on it.

Open the Terminal (on Mac/Linux) or Command Prompt (on Windows).

On Mac, press Command + Space, type Terminal, and hit Enter.

On Windows, press the Windows key, type cmd, and hit Enter.

Type or copy-paste the following commands:

Terminal

```bash
git clone https://github.com/AustinMusuya/event_api_capstone.git
```

Press Enter. This will download the project into a folder called even_api_capstone.

Navigate to the project folder by typing:

Terminal

```bash
cd event-_pi_capstone
```

2. **Create a Virtual Environment**

Create & activate a Virtual Environment

Terminal

```bash
# On Mac or Linux use: 
python3 -m venv venv
source venv/bin/activate   
```

```bash
# On Windows use: 
python -m venv venv
venv/Scripts/activate
```

3. **Install Dependancies**

   Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. **Configure the Database**

   Set up your MySQL database (or SQLite for development). Update the DATABASES configuration in `event_project/settings.py` 

For MySQL Database settings:

```python
DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': 'event_db',
      'USER': 'your-username',
      'PASSWORD': 'your-password',
      'HOST': 'localhost',
      'PORT': '3306',
      }
   }
```

OR

For SQLite Database settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

5. **Apply Migrations**

   Run the migrations to set up the database schema:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

6. **Create a Superuser (Admin)**

   Create a superuser to manage the app via Django admin:

```bash
python manage.py createsuperuser
```

7. **Run the Development Server**

   Start the Django development server to test the API:

```bash
python manage.py runserver
```

The API should now be running at http://127.0.0.1:8000/.

8. **Testing the API**

    To test the API, use tools like Rest Client (my personal favourite), Postman or CURL, or navigate to the API endpoints.


# API Endpoints


### List All Events
**Endpoint:** `GET /api/events/list-event`  
**Description:** Retrieves a list of all events.

---

### Get Event Details
**Endpoint:** `GET /api/events/<id>`  
**Description:** Retrieves details for a specific event.  
**Path Parameters:**
- `id` (string): The unique identifier of the event.

---

### List Upcoming Events
**Endpoint:** `GET /api/events/upcoming`  
**Description:** Retrieves a list of upcoming events.

---

### Create a New Event
**Endpoint:** `POST /api/events/create-event`  
**Description:** Creates a new event.  
**Request Body:**  
```json
{
  "name": "string",
  "date": "string",
  "location": "string",
  "description": "string"
}
            
   
 
