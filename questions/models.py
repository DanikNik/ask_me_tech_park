from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django import forms


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(to='Tag', related_name='questions')
    liked = models.ManyToManyField(to=User, related_name="liked_questions")

    # date = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', args=[self.pk])

    # def get_by_tag(self, tag):
    #     return Question.objects.filter(tags__text__exact=tag)


class Tag(models.Model):
    text = models.SlugField(unique=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', null=True, on_delete=models.CASCADE)

    @classmethod
    def answer_question(self, _question, _person, _text):
        answer = self.objects.create(author=_person, question=_question, rating=0, is_correct=False, text=_text)
        return answer

    def __str__(self):
        return '--'.join([self.author.username, self.question.title])


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter your genious answer!'}), label='')


class QuestionLike(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


# TODO novalidate в рендере формы валидация на стороне сервера
class QuestionCreationForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title:'}),
                            label='',
                            required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'Text of your question:'}),
                           label='',
                           required=True)
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          queryset=Tag.objects.all(),
                                          label='Tags')
