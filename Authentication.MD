

# Authentication Setup

# Overview
This project implements token-based authentication to secure API endpoints. The authentication system ensures that only authenticated users can access certain endpoints, such as creating, updating, or deleting events.

**SCREENSHOTS ARE IN THE FOLDER CALLED SCREENSHOTS IN REPOSITORY.**

# Authentication Flow

User Registration: A user registers using their username, email, and password. Upon successful registration, a token is generated and returned to the user.

User Login: The user can log in using their credentials (username and password). A token is generated and returned for subsequent requests.

Token Usage: The token is passed in the Authorization header as a Bearer token for authenticated requests.

User Logout: The user can log out by invalidating the token, ensuring no further access without re-authentication.

# Authentication Implementation Steps


1. **Install Required Libraries**

Install the required dependencies to implement authentication requirements.txt file:

```bash
    pip install -r requirements.txt
```

2. **Update Django Settings**

In your settings.py, add the following apps:

```python
INSTALLED_APPS = [
    # Other apps
    'rest_framework',
    'rest_framework.authtoken',
]
```


**Authentication settings**

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
}
```

3. **Create Serializer Classes for Authentication**

User Registration & Login

In your serializers.py, create a registration & login serializer classes:

```python
from django.contrib.auth import get_user_model
from .models import Event
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {"password": {"write_only":True}}


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def save(self, **kwargs):
        new_user = User.objects.create_user(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            password = self.validated_data['password']
        )

        new_user.save()
        # Generate token for the new user
        token = Token.objects.get_or_create(user=new_user)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']

```

4. **Create Authentication Views**

User Registration

In your views.py, create a registration view:

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import views, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, RegisterUserSerializer, UserSerializer


class RegisterUserAPIView(views.APIView):
    serializer_class = RegisterUserSerializer

    def get(self, request):
        return Response(
            {
                'message': 'Use POST request with username, email & password to register new user'
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=request.data['username'])
            token = Token.objects.get(user=user)

            serializer = self.serializer_class(user)

            return Response(
                {
                    'message': 'New user registration successful!',
                    'user': serializer.data,
                    'token': token.key
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
    
User Login
Next, create the login view.

```python
class LoginUserAPIView(views.APIView):
    serializer_class = LoginSerializer

    def get(self, request):
        return Response(
            {
                "message": "Use POST request with email & password to login user"
            },
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )

            if user:
                authenticated_user = User.objects.get(username=request.data['username'])

                serializer = UserSerializer(authenticated_user)

                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        'message': 'user logged in successfully!',
                        'user': serializer.data,
                        'token': token.key
                    },
                    status=status.HTTP_200_OK
                )

        return Response({'Message': 'Invalid Username and Password'}, status=status.HTTP_401_UNAUTHORIZED)
```    


**Add the following to your urls.py**

```python
urlpatterns = [

    # views for user registration and login
    path('users/register/',views.RegisterUserAPIView.as_view(),name="register"),
    path('users/login/',views.LoginUserAPIView.as_view(),name="login"),
    path('users/logout/',views.LogoutAPIView.as_view(),name="logout"),

]
```

5. **Protect API Endpoints**

To protect endpoints, use the IsAuthenticated permission class:

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, authenticate


class EventListAPIView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    return Response({'message': 'This is a protected view.'})
```

In this example, only authenticated users can access the protected_view.


6. **User Logout**

For logout functionality, doesn’t require explicit logout functionality (since the token is simply invalidated after expiry), you can implement logout by allowing token deletion on the client side.

Here’s an example view that can be used for logging out:

In your views.py file

```python
class LogoutAPIView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()

        return Response(
            {
                'message': "user logged out successfully!"
            },
            status=status.HTTP_200_OK
        )
```


# API Endpoints

### Setting Up Authorization in Postman
1. Go to the **Authorization** tab in Postman.
2. Select **OAuth 2.0** as the type.
3. Next, go to the **Headers** tab and add the following:
   - **Key:** `Authorization`
   - **Value:** `Token <generated-token>`

---

### How to Test Authentication Endpoints

1. **Register a User**

**Endpoint:** `POST /api/users/register/`  
**Description:** Registers a new user and creates a token.


**Request Body:** 

```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
    "message": "New user registration successful!",
    "user":
    {
        "id": 1,
        "username": "example_user",
        "email": "user@example.com"
    },
    "token": "generated-authentication-token"
}
```

2. **Login a User**

**Endpoint:** `POST /api/users/login/`  
**Description:** Logs in a user & creates or retrieves a token.


**Request Body:**  

```json
{
  "username": "example_user",
  "password": "securepassword"
}
```

**Response:**

```json
{
    "message": "user logged in successfully!",
    "user":
    {
        "id": 1,
        "username": "example_user",
        "email": "user@example.com"
    },
    "token": "generated-authentication-token"
}
```

3. **Logout a User**

**Endpoint:** `GET /api/users/logout/`  
**Description:** Logs out a user & deletes their token.


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
  "message": "user logged out successfully!"
}
```
### How to Test Event Management Endpoints

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