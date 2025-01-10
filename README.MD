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

5. **REST Client Extention on (VS Code)(Highly Recommended)**  
   Use a REST Client extention on vs code to test api endpoints. There's a sample.http file that has already been prepared for you to carry out api tests. 
   
   However you are still free to use Postman or Curl.

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
cd event_api_capstone
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
**Endpoint:** `GET /api/events/list-events/`  
**Description:** Retrieves a list of all events.

**Request Body:**  
```bash
Headers

  {
    Authorization: Token `generated-authentication-token`
  }
```

**Response:**

```json
{
  "id": 1,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price":0.00,
  "tags":["event", "firstEvent"], // add a list of tags in string format
  "location":"Event Location",
}

{
  "id": 2,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price":1000.00,
  "tags":["event", "firstEvent"],
  "location":"Event Location",
}

{
  "id": 3,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price":1000.00,
  "tags":["event", "firstEvent"], // add a list of tags in string format
  "location":"Event Location",
}

{
  "id": 4,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price":1000.00,
  "tags":["event", "firstEvent"],
  "location":"Event Location",
}
```

### Get Event Details
**Endpoint:** `GET /api/events/<int:pk>/`  
**Description:** Retrieving details of a specific event will require a token from the authenticated user. 
**Path Parameters:**
- `id` (string): The unique identifier of the event.

**Request Body:**  
```bash
Headers

  {
    Authorization: Token `generated-authentication-token`
  }
```

**Response:**
```json
{
  "id": 2,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price":0.00,
  "tags":["event", "firstEvent"],
  "location":"Event Location",
}
```

### List Upcoming Events
**Endpoint:** `GET /api/events/upcoming/`  
**Description:** Retrieves a list of upcoming events.

**Request Body:**  
```bash
Headers

  {
    Authorization: Token `generated-authentication-token`
  }
```

**Response:**

```json
{
  "id": 1,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price":0.00,
  "tags":["event", "firstEvent"],
  "location":"Event Location",
}

{
  "id": 2,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price":1000.00,
  "tags":["event", "firstEvent"],
  "location":"Event Location",
}
```

### Create a New Event
**Endpoint:** `POST /api/events/create-event/`  
**Description:** A new event will require a token key from the authenticated user to create the event.  
**Request Body:**  

```bash
Headers

  {
    Authorization: Token `generated-authentication-token`
  }
```

```json
{
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price": 500.00,
  "tags":["event", "firstEvent"],
  "location":"Event Location",
}
```

**Response:**

```json
{
"event":
   {
      "id": 1,
      "title": "Event Title",
      "description": "Event Description",
      "date": "2024-12-01 14:00:00",
      "ticket_price": 500.00,
      "tags":["event", "firstEvent"],
      "location":"Event Location",
   },
"message": "New event created successfully!"
}
```
            
   
### Update an Event
**Endpoint:** `PUT /api/events/<int:pk>/edit/`  
**Description:** An existing event will require a token key from the authenticated user to edit or update the event.  
**Request Body:**  

```bash
Headers

  {
    Authorization: Token `generated-authentication-token`
  }
```

```json
{
  "id": 1,
  "title": "Edited Event Title",
  "description": "Edited Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price": 500.00,
  "tags":["event", "firstEvent"],
  "location":"Edited Event Location",
}
```

**Response:**

```json
{
"event":
   {
      "id": 1,
      "title": "Edited Event Title",
      "description": "Edited Event Description",
      "date": "2024-12-01 14:00:00",
      "ticket_price": 500.00,
      "tags":["event", "firstEvent"],
      "location":"Edited Event Location",
   },
"message": "Event updated successfully!"
}
```

### Delete an Existing Event
**Endpoint:** `DELETE /api/events/<int:pk>/delete/`  
**Description:** An existing event will require a token key from the authenticated user to delete the existing event.  
**Request Body:**  

```bash
Headers

  {
    Authorization: Token `generated-authentication-token`
  }
```

```json
{
  "id": 1,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-01 14:00:00",
  "ticket_price": 500.00,
  "tags":["event", "firstEvent"],
  "location":"Event Location",
}
```

**Response:**

```json
{

"message": "Event deleted successfully!"

}
```


