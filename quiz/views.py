from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from classroom.models import Course
from module.models import Module
from completion.models import Completion
from .models import Quiz, QuizQuestion, QuizAnswer, Attempt
from .forms import AddQuizForm, AddQuizQuestionForm


@login_required
def add_quiz(request, course_slug, module_id):
    """
    Take course's slug and module's id, and add new quiz for this module.
    """
    course = get_object_or_404(Course, slug=course_slug)
    module = get_object_or_404(Module, pk=module_id)
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:    
        if request.method == "POST":
            form = AddQuizForm(request.POST)
            if form.is_valid():
                quiz_form = form.save(commit=False)
                quiz_form.teacher = request.user
                quiz_form.module = module
                quiz_form.save()
                # Display success message.
                messages.success(request, f'New quiz "{quiz_form.title}" has been added successfully.', extra_tags='add-quiz')
                return redirect(quiz_form.get_add_question_absolute_url())
        else:
            form = AddQuizForm()        
        context = {'form':form}
        return render(request, 'quiz/add_quiz.html', context)

@login_required
def add_question(request, course_slug, quiz_id):
    """
    Take course's slug and quiz's id, and add new question for this quiz.
    """
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:
        if request.method == "POST": 
            form = AddQuizQuestionForm(request.POST)
            if form.is_valid():
                question_form = form.save(commit=False)
                question_form.teacher = request.user
                question_form.quiz = quiz
                question_form.save()
                # Display success message.
                messages.success(request, f'New question has been added successfully.', extra_tags='add-question')
                # get answers.
                answer_text = request.POST.getlist('answer_text')
                is_correct = request.POST.getlist('is_correct')
                for a, c in zip(answer_text, is_correct):
                    answer = Answer.objects.create(answer_text=a, is_correct=c, question=question_form)
                return redirect(quiz.get_add_question_absolute_url())
        else:
            form = AddQuizQuestionForm()        
        context = {'form':form}
        return render(request, 'quiz/add_question.html', context)       

@login_required
def quiz_detail(request, course_slug, quiz_id):
    """
    Take course's slug and quiz's id, and display quiz detail with current student's attempts.
    """
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    student_attempts = Attempt.objects.filter(quiz=quiz, student=request.user)
    is_student = False
    if request.user in course.students.all():
        is_student = True
    context = {'quiz':quiz, 'student_attempts':student_attempts, 'is_student':is_student}
    return render(request, 'quiz/quiz_detail.html', context)

@login_required
def take_quiz(request, course_slug, quiz_id):
    """
    """
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    earned_points = 0
    is_student = False
    if request.user in course.students.all():
        is_student = True
    if not is_student:
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            questions = request.POST.getlist('question')
            answers = request.POST.getlist('answer')
            attempt = Attempt.objects.create(quiz=quiz, student=request.user, score=0)
            for q, a in zip(questions, answers):
                question = get_object_or_404(Question, pk=q)
                answer = get_object_or_404(Answer, pk=a)
                attempt.question.add(question)
                attempt.answer.add(answer)
                if answer.is_correct:
                    earned_points += question.points
                    attempt.score += earned_points
                    attempt.save()
            # create quiz completion
            c, created = Completion.objects.get_or_create(course=course, student=request.user, quiz=quiz)       
            return redirect(attempt.get_absolute_url())
        context = {'quiz':quiz, 'is_student':is_student}
        return render(request, 'quiz/take_quiz.html', context)

@login_required
def attempt_detail(request, course_slug, quiz_id, attempt_id):
    """
    """
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    attempt = get_object_or_404(Attempt, id=attempt_id)
    context = {'quiz':quiz, 'attempt':attempt}
    return render(request, 'quiz/attempt_detail.html', context)                