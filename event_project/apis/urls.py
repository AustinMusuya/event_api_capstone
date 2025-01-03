from django.urls import path, include
from . import views

urlpatterns = [
    # path('events/create-event',views.CreateEventAPIView.as_view(),name="create-event"),
    # path('events/list-event',views.CreateEventAPIView.as_view(),name="list-event"),
    # path('events/<int:id>',views.CreateEventAPIView.as_view(),name="detail-event"),
    # path('events/upcoming',views.CreateEventAPIView.as_view(),name="upcoming-events"),

    # views for user registration, login & logout
    path('users/register/',views.RegisterUserAPIView.as_view(),name="register"),
    path('users/login/',views.LoginUserAPIView.as_view(),name="login"),
    path('users/logout/',views.LogoutAPIView.as_view(),name="logout"),
    
]
