

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

# How to Test Authentication

1. **Register a User**

Use Postman, Curl or Rest Client (my personal favourite) to send a POST request to the /api/users/register/ endpoint with the following body:

```bash
json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "securepassword"
}
Response:

json
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

Send a POST request to the /api/users/login/ endpoint with the following body:


```bash
json
{
  "username": "example_user",
  "password": "securepassword"
}
Response:

json
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

Send a POST request to /api/users/logout/ with the token in the body to invalidate the session:

```bash
json
{
  "token": "generated-authentication-token"
}
Response:

json
{
  "message": "user logged out successfully!"
}
```

4. **Access Protected Endpoints**

Use the generated token to access protected endpoints. Send a GET request to the /api/events/ or any other protected endpoint, including the token in the Authorization header as a Bearer token:

```bash
curl -X GET /api/events/ -H "Authorization: Token *your-auth-token*"
```
