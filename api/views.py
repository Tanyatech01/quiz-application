from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Quiz, Question, Answer, Result

def home_page(request):
    quizzes = Quiz.objects.all()
    user_results = None
    
    # If the user is logged in, fetch only their scores
    if request.user.is_authenticated:
        user_results = Result.objects.filter(student=request.user).order_by('-date_taken')
        
    return render(request, 'home.html', {
        'all_quizzes': quizzes,
        'user_results': user_results
    })

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        score = 0
        total_questions = quiz.question_set.count()

        for question in quiz.question_set.all():
            selected_id = request.POST.get(f'question_{question.id}')
            
            if selected_id:
                selected_answer = question.answer_set.get(id=selected_id)
                if selected_answer.is_correct:
                    score += 1
        
        # Ensure the user is actually logged in before trying to save their score
        if request.user.is_authenticated:
            Result.objects.create(
                student=request.user,
                quiz=quiz,
                score=score,
                total_questions=total_questions
            )
        
        return render(request, 'result.html', {
            'score': score, 
            'total': total_questions, 
            'quiz': quiz
        })

    return render(request, 'take_quiz.html', {'quiz': quiz})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')