from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from classroom.models import Course
from completion.models import Completion
from .models import Module
from .forms import AddModuleForm


@login_required
def course_modules(request, course_slug):
    """
    Take course's slug and display all modules for this course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    modules = Module.objects.filter(course=course)
    page_completions = Completion.objects.filter(course=course, student=request.user).values_list('page__pk', flat=True)
    quiz_completions = Completion.objects.filter(course=course, student=request.user).values_list('quiz__pk', flat=True)
    assignment_completions = Completion.objects.filter(course=course, student=request.user).values_list('assignment__pk', flat=True)
    is_teacher = False
    if request.user == course.teacher:
        is_teacher = True
    context = {'course':course, 'modules':modules, 'is_teacher':is_teacher,'page_completions':page_completions, 
        'quiz_completions':quiz_completions, 'assignment_completions':assignment_completions}
    return render(request, 'module/course_modules.html', context)

@login_required
def add_module(request, course_slug):
    """
    Take course's slug and add new module for this course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:    
        if request.method == "POST":
            form = AddModuleForm(request.POST)
            if form.is_valid():
                module_form = form.save(commit=False)
                module_form.teacher = request.user
                module_form.course = course
                module_form.save()
                # Display success message.
                messages.success(request, f'New module "{module_form.title}" has been added successfully.', extra_tags='add-module')
                return redirect('module:add-module')
        else:
            form = AddModuleForm()        
        context = {'form':form}
        return render(request, 'module/add_module.html', context)