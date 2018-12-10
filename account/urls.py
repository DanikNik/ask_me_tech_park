from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.UserUpdateView.as_view(), name='user_settings')
]