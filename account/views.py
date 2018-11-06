from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView

class UserUpdateView(UpdateView):
    model = User