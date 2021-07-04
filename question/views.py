from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from classroom.models import Course
from .models import Question, Answer
from .forms import AddQuestionForm, AddAnswerForm


@login_required
def add_course_question(request, course_slug):
    """
    Take course's slug, and add new question for this course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    if request.user == course.teacher or request.user in course.students.all():
        if request.method == "POST":
            form = AddQuestionForm(request.POST)
            if form.is_valid():
                question_form = form.save(commit=False)
                question_form.student = request.user
                question_form.course = course
                question_form.save()
                # Display success message.
                messages.success(request, f'Your question has been added successfully.', extra_tags='add-question')
                return redirect(course.get_questions_absolute_url())
        else:
            form = AddQuestionForm()        
        context = {'form':form}
        return render(request, 'question/add_question.html', context)
    else:    
        return HttpResponseForbidden()

@login_required
def course_questions(request, course_slug):
    """
    Take course's slug, and display all its questions.
    """
    course = get_object_or_404(Course, slug=course_slug)
    questions = Question.objects.filter(course=course)
    is_teacher = False
    if request.user == course.teacher:
        is_teacher = True
    # paginate questions
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    question_objs = paginator.get_page(page_number)
    context = {'course': course, 'questions': question_objs, 'is_teacher': is_teacher}
    return render(request, 'question/course_questions.html', context)

@login_required
def question_detail(request, course_slug, question_id):
    """
    Take course's slug and question's id, and dispaly this question destail.
    Add answer to this question.
    """
    course = get_object_or_404(Course, slug=course_slug)
    question = get_object_or_404(Question, id=question_id)
    if request.user == course.teacher or request.user in course.students.all():
        answers = Answer.objects.filter(question=question).order_by('-is_accepted_answer')
        is_teacher = False
        if request.user == course.teacher:
            is_teacher = True 
        moderator = False
        if is_teacher or request.user == question.student:
            moderator = True
        # add answer
        if request.method == "POST":
            form = AddAnswerForm(request.POST)
            if form.is_valid():
                answer_form = form.save(commit=False)
                answer_form.student = request.user
                answer_form.question = question
                answer_form.save()
                # Display success message.
                messages.success(request, f'Your answer has been added successfully.', extra_tags='add-answer')
                return redirect(question.get_absolute_url())
        else:
            form = AddAnswerForm()        
        context = {'course': course, 'question': question, 'answers': answers, 'moderator': moderator, 'form':form, 'is_teacher': is_teacher}
        return render(request, 'question/question_detail.html', context) 
    else:
        return HttpResponseForbidden()

@login_required
def mark_as_answer(request, course_slug, question_id, answer_id):
    """
    Take course's slug, question's id and answer's id, and set this answer to be accepted.
    """
    course = get_object_or_404(Course, slug=course_slug)
    question = get_object_or_404(Question, id=question_id)
    if request.user == course.teacher or request.user == question.student:
        answer = get_object_or_404(Answer, id=answer_id)
        answer.is_accepted_answer = True
        answer.save()
        question.has_accepted_answer = True
        question.save()
        return redirect(question.get_absolute_url())
    else:
        return HttpResponseForbidden() 
        
@login_required
def vote_answer(request, course_slug, question_id):
    """
    Take course's slug and question's id.
    Get answer's id and vote type by ajax, and vote this answer.
    """
    user = request.user
    course = get_object_or_404(Course, slug=course_slug)
    question = get_object_or_404(Question, id=question_id)
    if user == course.teacher or user in course.students.all():
        answer_id = request.POST.get('answer_id')
        vote_type = request.POST.get('vote_type')
        try:
            # answer = get_object_or_404(Answer, id=answer_id)
            answer = Answer.objects.get(id=answer_id)
            if vote_type == 'U':
                answer.up_votes.add(user)
                if user in answer.down_votes.all():
                    answer.down_votes.remove(user)
            elif vote_type == 'D': 
                answer.down_votes.add(user)
                if user in answer.up_votes.all():
                    answer.up_votes.remove(user)
            return HttpResponse(answer.calculate_votes)
        except Exception as e:
            raise e
    else:
        return HttpResponseForbidden() 
        