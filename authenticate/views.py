from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse



class RegisterFormView(FormView):
    form_class = UserCreationForm

    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        print(user)
        login(self.request, user)
        self.success_url = reverse("question_list")
        return super(RegisterFormView, self).form_valid(form)
