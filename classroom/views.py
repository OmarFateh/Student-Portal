from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from .models import Category, Course, Grade
from .forms import AddCourseForm


def categories(request):
    """
    Display all categories.
    """ 
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'classroom/categories.html', context)

def category_courses(request, category_slug):
    """
    Take a category's slug, and display all courses of this category.
    """
    # Comment.objects.select_related('owner', 'item', 'reply').prefetch_related('likes')
    category = get_object_or_404(Category, slug=category_slug)
    courses = category.courses.all()
    context = {'category':category, 'courses':courses}
    return render(request, 'classroom/category_courses.html', context)

def course_detail(request, course_slug):
    """
    Take course's slug, and get the course detail.
    """
    course = get_object_or_404(Course, slug=course_slug)
    is_teacher = False
    if request.user == course.teacher:
        is_teacher = True
    context = {'course':course, 'is_teacher':is_teacher}
    return render(request, 'classroom/course_detail.html', context)

@login_required
def add_course(request):
    """
    Add new course.
    """
    if request.method == "POST":
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course_form = form.save(commit=False)
            course_form.teacher = request.user
            course_form.save()
            # Display success message.
            messages.success(request, f'New course "{course_form.title}" has been added successfully.', extra_tags='add-course')
            return redirect('classroom:add-course')
    else:
        form = AddCourseForm()        
    context = {'form':form}
    return render(request, 'classroom/add_course.html', context)

@login_required
def update_course(request, course_slug):
    """
    Take course's id, and update this course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:    
        if request.method == "POST":
            form = AddCourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('classroom:my-courses')    
        else:
            form = AddCourseForm(instance=course)        
        context = {'form':form, 'course':course}
        return render(request, 'classroom/update_course.html', context)

@login_required
def delete_course(request, course_slug):
    """
    Take course's slug, and delete this course if the requested user is the teacher of the course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:
        course.delete()
    return redirect('classroom:my-courses')

@login_required
def my_courses(request):
    """
    Display all the current user's teaching courses.
    """
    courses = Course.objects.filter(teacher=request.user)
    context = {'courses':courses}
    return render(request, 'classroom/my_courses.html', context)

@login_required
def enroll_course(request, course_slug):
    """
    Take course's slug, and enroll student to this course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    if request.user not in course.students.all():
        course.students.add(request.user)
        # Display success message.
        messages.success(request, f'You have enrolled to the course "{course.title}" successfully.', extra_tags='enroll-course')
        return redirect(course.get_absolute_url())

@login_required
def course_grades(request, course_slug):
    """
    Take course's slug, and display all course's grades if the user is the teacher of the course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:
        is_teacher = True    
        grades = Grade.objects.filter(course=course)
        context = {'course':course, 'grades':grades, 'is_teacher':is_teacher}
        return render(request, 'classroom/course_grades.html', context)  

@login_required
def student_grades(request, course_slug):
    """
    Take course's slug, and display student's grades if the user is student in this course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    if request.user not in course.students.all():
        return HttpResponseForbidden()
    else:
        is_teacher = False
        if request.user == course.teacher:
            is_teacher = True    
        grades = Grade.objects.filter(course=course, submission__student=request.user)
        context = {'course':course, 'grades':grades, 'is_teacher':is_teacher}
        return render(request, 'classroom/student_grades.html', context)

@login_required
def grade_submission(request, course_slug, grade_id):
    """
    Take course's slug and grade's id, and grade the submitted assignment if the user is the teacher of the course.
    """
    course = get_object_or_404(Course, slug=course_slug)
    grade = get_object_or_404(Grade, id=grade_id)
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            points = request.POST.get('points')
            grade.points = points
            grade.status = 'graded'
            grade.save()
            return redirect(course.get_course_submissions_absolute_url())
        context = {'course': course, 'grade': grade,}
        return render(request, 'classroom/grade_submission.html', context)
