from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.RegisterFormView.as_view(), name='register'),
    # path('new_person/', views.NewPersonView.as_view(), name='new_person'),
    # path('login/', views.LoginFormView.as_view()),
]