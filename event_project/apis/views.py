from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Event
from .permissions import IsAuthorOrReadOnly
from rest_framework import views, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, RegisterUserSerializer, EventSerializer, UserSerializer, CreateEventSerializer
from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
User = get_user_model()
class RegisterUserAPIView(views.APIView):
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Use this endpoint to register a new user by providing username, email, and password.",
        responses={200: "OK"}
    )
    def get(self, request):
        return Response(
            {
                'message': 'Use POST request with username, email & password to register new user'
            },
            status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Creates a new user account and returns user details plus JWT tokens.",
        request_body=RegisterUserSerializer,
        responses={
            201: openapi.Response(
                description="Successful Registration",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "email": openapi.Schema(type=openapi.TYPE_STRING, example="user@example.com"),
                        "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
                        "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe"),
                        "tokens": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                        ),
                    },
                ),
            )
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=request.data['username'])
            token = Token.objects.get(user=user)

            user_serializer = self.serializer_class(user)

            return Response(
                {
                    'message': 'New user registration successful!',
                    'user': user_serializer.data,
                    'token': token.key
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserAPIView(views.APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="Login a user",
        operation_description="Use this endpoint to login a user by providing username and password.",
        responses={200: "OK"}
    )
    def get(self, request):
        return Response(
            {
                "message": "Use POST request with username & password to login user"
            },
            status=status.HTTP_200_OK
        )
    
    @swagger_auto_schema(
            operation_summary="User Login",
            operation_description="Authenticates a user and returns user details along with an authentication token.",
            request_body=LoginSerializer,
            responses={
                200: openapi.Response(
                    description="Successful Login",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "message": openapi.Schema(type=openapi.TYPE_STRING, example="user logged in successfully!"),
                            "user": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                    "username": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe"),
                                    "email": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe@example.com"),
                                },
                            ),
                            "token": openapi.Schema(type=openapi.TYPE_STRING, example="token_here"),
                        },
                    ),
                ),
                401: openapi.Response(
                    description="Invalid Credentials",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "Message": openapi.Schema(type=openapi.TYPE_STRING, example="Invalid Username and Password"),
                        },
                    ),
                ),
            }
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

                # Use the UserSerializer class instead to return response that doesn't show the user password.
                user_serializer = UserSerializer(authenticated_user)

                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        'message': 'user logged in successfully!',
                        'user': user_serializer.data,
                        'token': token.key
                    },
                    status=status.HTTP_200_OK
                )

        return Response({'Message': 'Invalid Username and Password'}, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutAPIView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="User Logout",
        operation_description="Logs out the authenticated user by deleting their authentication token.",
        responses={
            200: openapi.Response(
                description="Successful Logout",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="user logged out successfully!"),
                    },
                ),
            ),
        }
    )
    def get(self, request):
        request.user.auth_token.delete()

        return Response(
            {
                'message': "user logged out successfully!"
            },
            status=status.HTTP_200_OK
        )
    

# APIView to List all events
class ListEventAPIView(views.APIView):
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all events",
        operation_description="Retrieves a list of all events. Optionally, filter events by tags using query parameters.",
        manual_parameters=[
            openapi.Parameter(
                'tags', openapi.IN_QUERY,
                description="Filter events by tags. Use multiple 'tags' parameters to filter by multiple tags.",
                type=openapi.TYPE_STRING,
                required=False,
                example="music"
            ),
        ],
        responses={200: "OK"}
    )
    def get(self, request):
        events = Event.objects.all()


        # Get tags from query params
        tags = request.query_params.getlist('tags')  # For multiple tags

        if tags:
            events = events.filter(tags__name__in=tags).distinct() # Filter entries by tags

        if events.exists():
            serializer = self.serializer_class(events, many=True)

            return Response(
                {
                    'events':serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response({'Message': 'No event records available'}, status=status.HTTP_404_NOT_FOUND)
    
# APIView to List all upcoming events
class ListEventUpcomingAPIView(views.APIView):
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all upcoming events",
        operation_description="Retrieves a list of all upcoming events. Optionally, filter events by tags using query parameters.",
        manual_parameters=[
            openapi.Parameter(
                'tags', openapi.IN_QUERY,
                description="Filter events by tags. Use multiple 'tags' parameters to filter by multiple tags.",
                type=openapi.TYPE_STRING,
                required=False,
                example="music"
            ),
        ],        
        responses={200: "OK"}
    )
    def get(self, request):
        events = Event.objects.filter(date__gt=now())

        # Get tags from query params
        tags = request.query_params.getlist('tags')  # For multiple tags

        if tags:
            events = events.filter(tags__name__in=tags).distinct() # Filter entries by tags

        if events.exists():
            serializer = self.serializer_class(events, many=True)

            return Response(
                {
                    'events':serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response({'Message': 'No event records available'}, status=status.HTTP_404_NOT_FOUND)

# APIView to Create an event
class CreateEventAPIView(views.APIView):
    serializer_class = CreateEventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                'message': 'Use POST request with title, description, date, location & ticket_price to create a new event.'
            },
            status=status.HTTP_200_OK
        )
    
    @swagger_auto_schema(
        operation_summary="Create a new event",
        operation_description="Creates a new event with the provided details. The authenticated user will be set as the organizer.",
        request_body=CreateEventSerializer,
        responses={
            201: openapi.Response(
                description="Event Created Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "event": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "title": openapi.Schema(type=openapi.TYPE_STRING, example="Sample Event"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, example="This is a sample event description."),
                                "date": openapi.Schema(type=openapi.FORMAT_DATETIME, example="2023-12-31T20:00:00Z"),
                                "location": openapi.Schema(type=openapi.TYPE_STRING, example="New York"),
                                "ticket_price": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=50.00),
                                "tags": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), example=["music", "festival"]),
                                "organizer": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            },
                        ),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="New event created successfully!"),
                    },
                ),
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user) 

            event = Event.objects.get(title=request.data['title'])

            new_event_serializer = self.serializer_class(event)

            return Response(
                {
                    'event': new_event_serializer.data,
                    'message': "New event created successfully!"
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# APIView to Retrieve, Update & Delete a specific event   
class RetrieveUpdateDeleteEventAPIView(views.APIView):
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def get_object(self, pk):
        try:
            obj = Event.objects.get(pk=pk)
            # Enforce object-level permission
            self.check_object_permissions(self.request, obj)
            return obj
        except Event.DoesNotExist:
            return Response({'Message': 'No event record available'}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_summary="Retrieve, update, or delete an event",
        operation_description="Retrieve, update, or delete an event by its ID. Only the organizer can update or delete the event.",
        responses={200: "OK"}
    )
    def get(self, request, pk, format=None):
        Event = self.get_object(pk)
        serializer = EventSerializer(Event)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Update an event",
        operation_description="Updates the details of an existing event. Only the organizer can update the event.",
        request_body=EventSerializer,
        responses={
            200: openapi.Response(
                description="Event Updated Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "event": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "title": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Event"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, example="This is an updated event description."),
                                "date": openapi.Schema(type=openapi.FORMAT_DATETIME, example="2023-12-31T20:00:00Z"),
                                "location": openapi.Schema(type=openapi.TYPE_STRING, example="Los Angeles"),
                                "ticket_price": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=75.00),
                                "tags": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), example=["art", "exhibition"]),
                                "organizer": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            },
                        ),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Event updated successfully!"),
                    },
                ),
            ),
            204: openapi.Response(
                description="Event Deleted Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Event deleted successfully!"),
                    },
                ),
            ),
        }   
    )
    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "event" : serializer.data,
                    "message": "Event updated successfully!"
                },
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Delete an event",
        operation_description="Deletes an existing event. Only the organizer can delete the event.",
        responses={
            204: openapi.Response(
                description="Event Deleted Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Event deleted successfully!"),
                    },
                ),
            ),
        }
    )
    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(
            {
                "message": "Event deleted successfully!"
            },
            status=status.HTTP_204_NO_CONTENT
        )

