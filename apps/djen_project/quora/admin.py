from django.contrib import admin
from .models import CustomUser, Questions, Answers

class AnswerInline(admin.TabularInline):
    model = Answers

class QuestionsAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]
    class Meta:
        model = Questions

class CustomUserAdmin(admin.ModelAdmin):

    class Meta:
        model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Questions, QuestionsAdmin)