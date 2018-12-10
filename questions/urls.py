from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('tag/<slug:tag_name>', views.QuestionByTagView.as_view(), name='question_by_tag'),
    path('create/', views.QuestionCreateView.as_view(), name='question_create'),

]