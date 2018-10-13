from django.views.generic import TemplateView

class QuestionListView(TemplateView):
    template_name = 'questions/question_list.html'