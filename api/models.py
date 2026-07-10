from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    quiz_name = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    time_limit = models.IntegerField()

    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
    
class Result(models.Model):
    # Links the score to the built-in Django User (the student)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    # Links the score to the specific quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    # Automatically saves the exact date and time the quiz was finished
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.quiz_name} - {self.score}/{self.total_questions}"    