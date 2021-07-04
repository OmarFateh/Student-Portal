from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from module.models import Module
from userprofile.models import BaseTimestamp

from ckeditor.fields import RichTextField

User = get_user_model()


def assignment_file(instance, filename):
    """
    Upload the assignment file into the path and return the uploaded file path.
    """
    return f'Courses/assignments/{instance.teacher.full_name}/{filename}'

def submission_file(instance, filename):
    """
    Upload the submission file into the path and return the uploaded file path.
    """
    return f'Courses/assignments/{instance.assignment.title}/submissions/{instance.student.full_name}/{filename}'    

class AssignmentFiles(BaseTimestamp):
    """
    A relationship model between the page and its files.
    """
    file = models.FileField(upload_to=assignment_file)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Return teacher's fullname.
        return f"{self.teacher.full_name}"

    def get_filename(self):
        return self.file.name.split('/')[-1]


class Assignment(BaseTimestamp):
    """
    Assignment model.
    """
    title = models.CharField(max_length=200)
    content = RichTextField()
    points = models.PositiveIntegerField()
    due = models.DateField()
    teacher = models.ForeignKey(User, related_name='assignments', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='assignments', on_delete=models.CASCADE)
    files = models.ManyToManyField(AssignmentFiles, blank=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        # Return assignment's title, module's title and course's title.
        return f"{self.title} | {self.module.title} | {self.module.course.title}"

    def get_absolute_url(self):
        # Return absolute url of assignment by its id.
        return reverse("assignment:assignment-detail", kwargs={"course_slug": self.module.course.slug, "assignment_id": self.id})

    def get_add_submission_absolute_url(self):
        # Return add submission absolute url of assignment by its id.
        return reverse("assignment:submit-assignment", kwargs={"course_slug": self.module.course.slug, "assignment_id": self.id})


class Submission(BaseTimestamp):
    """
    Submission model.
    """
    student = models.ForeignKey(User, related_name='assignment_submissions', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    file = models.FileField(upload_to=submission_file)
    comment = models.TextField()

    def __str__(self):
        # Return assignment's title and student's full name.
        return f"{self.assignment.title} | {self.student.full_name}"

    def get_filename(self):
        return self.file.name.split('/')[-1]