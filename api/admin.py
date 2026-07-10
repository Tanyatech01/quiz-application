from django.contrib import admin
from .models import Quiz, Question, Answer,Result

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Shows 4 blank answer slots by default

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
