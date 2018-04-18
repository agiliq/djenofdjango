from django.shortcuts import render

# Create your views here.

class AddQuestionView(FormView):

    def get(self, request):
        content = {}
        template = "questions.html"
        return render(request, template, content)
