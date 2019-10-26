from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('tag/<slug:tag_name>', views.QuestionByTagView.as_view(), name='question_by_tag'),
    path('create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('rate_question/', views.rate_question, name='rate_question'),
    path('rate_answer/', views.rate_answer, name='rate_answer'),
    path('update_answers/', views.update_answers, name='update_answers')

]
