import jwt
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, FormMixin
from faker import Faker
from django.http import HttpResponse

from django.db import transaction

from .models import Question, Tag, Answer, QuestionCreationForm, AnswerForm, QuestionLike, AnswerLike

from cent import Client

fake = Faker()

cl = Client("http://127.0.0.1:8048/", "api_key", timeout=1)


class QuestionListView(ListView):
    template_name = 'questions/question_list.html'

    model = Question
    context_object_name = 'question_list'

    # ordering = 'title'
    paginate_by = 10

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

    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['tag_list'] = Tag.objects.all()
        return context

    def get_queryset(self):
        return Question.objects.filter(tags__text__exact=self.kwargs['tag_name'])


class QuestionDetailView(DetailView, FormMixin):
    template_name = 'questions/question_detail.html'
    model = Question

    context_object_name = 'question'
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tag_list'] = Tag.objects.all()
        # token = jwt.encode({"sub": str(self.request.user.id)}, "dd835d28-6e32-4ba3-81b2-547cecdb0dbb").decode()
        # context['token'] = token
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


class QuestionCreateView(FormView):
    template_name = 'questions/question_create.html'

    form_class = QuestionCreationForm

    def form_valid(self, form):
        question = Question.objects.create(title=form.cleaned_data['title'],
                                           text=form.cleaned_data['text'])
        question.tags.set(form.cleaned_data['tags'])
        question.author = self.request.user
        question.rating = 0
        question.save()
        self.success_url = question.get_absolute_url()

        return super(QuestionCreateView, self).form_valid(form)


@transaction.atomic
def rate_question(request):
    question_id = int(request.POST['id'])
    value = int(request.POST['value'])
    _question = Question.objects.get(id=question_id)
    _user = request.user
    try:
        like = QuestionLike.objects.get(question=_question, user=_user)
    except:
        like = None
    if like is not None:
        return HttpResponse(0, status=403)
    else:
        _question.rating += value
        _question.liked.add(_user)
        _question.save()
        QuestionLike.objects.create(question=_question, user=_user)
        return HttpResponse(_question.rating, status=200)


@transaction.atomic
def rate_answer(request):
    # cl.publish("news", {"hello": "world"})
    answer_id = int(request.POST['id'])
    value = int(request.POST['value'])
    # cl.publish("news", {"hello": "world"})
    _answer = Answer.objects.get(id=answer_id)
    _user = request.user
    try:
        like = AnswerLike.objects.get(answer=_answer, user=_user)
    except:
        like = None
    if like is not None:
        return HttpResponse(0, status=403)
    else:
        _answer.rating += value
        _answer.save()
        AnswerLike.objects.create(answer=_answer, user=_user)
        return HttpResponse(_answer.rating, status=200)

# TODO если проголосовал то делать кнопку неактивной
