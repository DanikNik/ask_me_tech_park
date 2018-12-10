from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormMixin
from faker import Faker

from questions.models import Question, Tag, Answer
from . import models

fake = Faker()


class QuestionListView(ListView):
    template_name = 'questions/question_list.html'

    model = models.Question
    context_object_name = 'question_list'

    # ordering = 'title'
    paginate_by = 8

    def get_queryset(self):
        return Question.objects.order_by('title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.request.GET.get('tag')
        if tag_name is not None:
            context['tag_query'] = tag_name
            context['question_list'] = Question.objects.filter(tags__text__exact=tag_name)
        # else:
        #     context['question_list'] = Question.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context


class QuestionByTagView(ListView):
    template_name = "questions/question_list.html"
    context_object_name = 'question_list'

    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['tag_list'] = Tag.objects.all()
        return context

    def get_queryset(self):
        return Question.objects.filter(tags__text__exact=self.kwargs['tag_name'])


class QuestionDetailView(DetailView, FormMixin):
    template_name = 'questions/question_detail.html'
    model = models.Question

    context_object_name = 'question'
    form_class = models.AnswerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # context['question'] = self.object
        context['tag_list'] = Tag.objects.all()
        return context

    def form_valid(self, form):
        answer = Answer.answer_question(self.object, self.request.user, form.cleaned_data['text'])
        answer.save()
        return super(QuestionDetailView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class QuestionCreateView(CreateView):
    template_name = 'questions/question_create.html'
    model = models.Question
    fields = [
        'title',
        'text',
        'tags'
    ]

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.rating = 0
        question.save()

        return super(QuestionCreateView, self).form_valid(form)
