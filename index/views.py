from django.views.generic import TemplateView
from faker import Faker

fake = Faker()

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['question_list'] = range(10)
        context['tag_list'] = fake.words(12)
        return context