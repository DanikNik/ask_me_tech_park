from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(to='Tag', related_name='questions')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', args=[self.pk])


class Tag(models.Model):
    text = models.SlugField(unique=True)


class Answer(models.Model):
    # title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
