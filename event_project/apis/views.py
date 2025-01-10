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

# Create your views here.
User = get_user_model()
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

    def get(self, request):
        return Response(
            {
                "message": "Use POST request with username & password to login user"
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
    
    def get(self, request, pk, format=None):
        Event = self.get_object(pk)
        serializer = EventSerializer(Event)
        return Response(serializer.data)
    
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
    
    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(
            {
                "message": "Event deleted successfully!"
            },
            status=status.HTTP_204_NO_CONTENT
        )

