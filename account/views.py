# from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic.edit import UpdateView
from questions.models import Tag

class UserUpdateView(UpdateView):
    template_name = 'account/user_settings.html'
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tag_list'] = Tag.objects.all()
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('question_list')