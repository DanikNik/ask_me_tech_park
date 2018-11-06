from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from faker import Faker
from . import models

fake = Faker()


class QuestionListView(ListView):
    template_name = 'questions/question_list.html'

    model = models.Question
    context_object_name = 'question_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # context['question_list'] = range(10)
        context['tag_list'] = fake.words(12)
        return context


class QuestionDetailView(DetailView):
    template_name = 'questions/question_detail.html'
    model = models.Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['question'] = self.object
        context['tag_list'] = fake.words(12)
        return context


class QuestionCreateView(CreateView):
    template_name = 'questions/question_create.html'
    model = models.Question
    fields = [
        'title',
        'text',
        'tags'
    ]
