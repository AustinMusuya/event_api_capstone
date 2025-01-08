from django.urls import path, include
from . import views

urlpatterns = [
    # views for user registration, login & logout
    path('users/register/',views.RegisterUserAPIView.as_view(),name="register"),
    path('users/login/',views.LoginUserAPIView.as_view(),name="login"),
    path('users/logout/',views.LogoutAPIView.as_view(),name="logout"),

    # CRUD views for events and users
    path('events/create-event/',views.CreateEventAPIView.as_view(),name="create-event"),
    path('events/list-events/',views.ListEventAPIView.as_view(),name="list-event"),
    path('events/<int:pk>/',views.RetrieveUpdateDeleteEventAPIView.as_view(),name="detail-event"),
    path('events/<int:pk>/edit/',views.RetrieveUpdateDeleteEventAPIView.as_view(),name="edit-event"),
    path('events/<int:pk>/delete/',views.RetrieveUpdateDeleteEventAPIView.as_view(),name="delete-event"),
    
    path('events/upcoming/',views.ListEventUpcomingAPIView.as_view(),name="upcoming-events"),

    
]
