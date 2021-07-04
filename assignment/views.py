from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from classroom.models import Course, Grade
from module.models import Module
from completion.models import Completion
from .models import AssignmentFiles, Assignment, Submission
from .forms import AddAssignmentForm, AddSubmissionForm


@login_required
def add_assignment(request, course_slug, module_id):
    """
    Take course's slug and module's id, and add new assignment for this module.
    """
    course = get_object_or_404(Course, slug=course_slug)
    module = get_object_or_404(Module, pk=module_id)
    files_objs = []
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:    
        if request.method == "POST":
            form = AddAssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist('files')
                for file in files:
                    new_file = AssignmentFiles.objects.create(file=file, teacher=request.user)
                    files_objs.append(new_file)
                assignment_form = form.save(commit=False)
                assignment_form.teacher = request.user
                assignment_form.module = module
                assignment_form.save()
                assignment_form.files.set(files_objs)
                # Display success message.
                messages.success(request, f'New assignment "{assignment_form.title}" has been added successfully.', extra_tags='add-assignment')
                return redirect(assignment_form.get_absolute_url())
        else:
            form = AddAssignmentForm()        
        context = {'form':form}
        return render(request, 'assignment/add_assignment.html', context)

@login_required
def assignment_detail(request, course_slug, assignment_id):
    """
    Take course's slug and assignment's id, and display assignment detail with current student's attempts.
    """
    course = get_object_or_404(Course, slug=course_slug)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    student_submissions = Submission.objects.filter(assignment=assignment, student=request.user)
    is_student = False
    if request.user in course.students.all():
        is_student = True
    context = {'assignment':assignment, 'student_submissions':student_submissions, 'is_student':is_student}
    return render(request, 'assignment/assignment_detail.html', context)        

@login_required
def submit_assignment(request, course_slug, assignment_id):
    """
    Take course's slug and assignment's id, and add new submission for this assignment.
    """  
    course = get_object_or_404(Course, slug=course_slug)
    assignment = get_object_or_404(Assignment, pk=assignment_id)  
    if request.user not in course.students.all():
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            form = AddSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission_form = form.save(commit=False)
                submission_form.student = request.user
                submission_form.assignment = assignment
                submission_form.save()
                Grade.objects.create(course=course, submission=submission_form, points=0)
                # create assignment completion
                c, created = Completion.objects.get_or_create(course=course, student=request.user, assignment=assignment)
                # Display success message.
                messages.success(request, f'Your submission has been added successfully.', extra_tags='add-submission')
                return redirect(assignment.get_absolute_url())
        else:
            form = AddSubmissionForm()        
        context = {'assignment':assignment, 'form':form}
        return render(request, 'assignment/submit_assignment.html', context)
