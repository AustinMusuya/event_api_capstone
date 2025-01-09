from django.contrib.auth import get_user_model
from .models import Event
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

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
        extra_kwargs = {"password": {"write_only":True}}

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
class EventSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'ticket_price', 'tags', 'organizer']
        extra_kwargs = {'organizer': {'read_only':True}}

class CreateEventSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'ticket_price', 'tags', 'organizer']
        extra_kwargs = {'organizer': {'read_only':True}}

        def validate(self, data):
            if data['date'] <= now():
                raise serializers.ValidationError("Date must be set in the future.")
            
            if data['ticket_price'] < 0.00:
                raise serializers.ValidationError("Ticket price cannot be less than 0.00!")
            
            return data

        def save(self, **kwargs):
            organizer = kwargs.get('organizer')

            new_event = Event.objects.create(
                title = self.validated_data['title'],
                description = self.validated_data['description'],
                date = self.validated_data['date'],
                location = self.validated_data['location'],
                ticket_price = self.validated_data['ticket_price'],
                tags= self.validated_data['tags'],
                organizer = organizer
            )

            new_event.save()

