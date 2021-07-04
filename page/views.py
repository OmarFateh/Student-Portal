from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from classroom.models import Course
from module.models import Module
from completion.models import Completion
from .models import PageFiles, Page
from .forms import AddPageForm


@login_required
def add_page(request, course_slug, module_id):
    """
    Take course's slug and module's id, and add new page for this module.
    """
    course = get_object_or_404(Course, slug=course_slug)
    module = get_object_or_404(Module, pk=module_id)
    files_objs = []
    if request.user != course.teacher:
        return HttpResponseForbidden()
    else:    
        if request.method == "POST":
            form = AddPageForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist('files')
                for file in files:
                    new_file = PageFiles.objects.create(file=file, teacher=request.user)
                    files_objs.append(new_file)
                page_form = form.save(commit=False)
                page_form.teacher = request.user
                page_form.module = module
                page_form.save()
                page_form.files.set(files_objs)
                # Display success message.
                messages.success(request, f'New page "{page_form.title}" has been added successfully.', extra_tags='add-page')
                return redirect(page_form.get_absolute_url())
        else:
            form = AddPageForm()        
        context = {'form':form}
        return render(request, 'page/add_page.html', context)

def page_detail(request, course_slug, page_id):
    """
    Take course's slug and page's id, and display page detail.
    """
    course = get_object_or_404(Course, slug=course_slug)
    page = get_object_or_404(Page, pk=page_id)
    completed = Completion.objects.filter(course=course, student=request.user, page=page).exists()
    context = {'course':course, 'page':page, 'completed':completed}
    return render(request, 'page/page_detail.html', context)

@login_required
def mark_page_as_done(request, course_slug, page_id):
    """
    Take course's slug and page's id, and mark page as done.
    """
    course = get_object_or_404(Course, slug=course_slug)
    page = get_object_or_404(Page, pk=page_id)
    c, created = Completion.objects.get_or_create(course=course, student=request.user, page=page)
    return redirect(page.get_absolute_url())    
