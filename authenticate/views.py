from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class RegisterFormView(FormView):
    form_class = UserCreationForm

    template_name = "registration/register.html"

    def form_valid(self, form):
        self.user = form.save()
        print(self.user)
        login(self.request, self.user)
        self.success_url = "/auth/login/"
        return super(RegisterFormView, self).form_valid(form)

# Create your views here.

#
# class LoginFormView(FormView):
#     form_class = AuthenticationForm
#
#     template_name = "registration/login.html"
#     success_url = '/events'
#     def form_valid(self, form):
#         self.user = form.get_user()
#
#         login(self.request, self.user)
#         self.success_url = '/account/'+str(self.user.id)
#         return super(LoginFormView, self).form_valid(form)
