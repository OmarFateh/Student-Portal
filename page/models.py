import os

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from module.models import Module
from userprofile.models import BaseTimestamp

from ckeditor.fields import RichTextField

User = get_user_model()


def course_file(instance, filename):
    """
    Upload the course file into the path and return the uploaded file path.
    """
    return f'Courses/{instance.teacher.full_name}/{filename}'

class PageFiles(BaseTimestamp):
    """
    A relationship model between the page and its files.
    """
    file = models.FileField(upload_to=course_file)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Return course's title
        return f"{self.course.title} | {self.teacher.full_name}"

    def get_filename(self):
        return self.file.name.split('/')[-1]


class Page(BaseTimestamp):
    """
    Page model.
    """
    title = models.CharField(max_length=200)
    content = RichTextField()
    teacher = models.ForeignKey(User, related_name='module_pages', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='pages', on_delete=models.CASCADE)
    files = models.ManyToManyField(PageFiles, blank=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        # Return page's title, module's title and course's title.
        return f"{self.title} | {self.module.title} | {self.module.course.title}"

    def get_absolute_url(self):
        # Return absolute url of page by its id.
        return reverse("page:page-detail", kwargs={"course_slug": self.module.course.slug, "page_id": self.id})

    def get_mark_done_absolute_url(self):
        # Return mark as done absolute url of page by its id.
        return reverse("page:mark-as-done", kwargs={"course_slug": self.module.course.slug, "page_id": self.id})    