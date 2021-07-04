from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from classroom.models import Course
from page.models import Page
from quiz.models import Quiz
from assignment.models import Assignment
from userprofile.models import BaseTimestamp

User = get_user_model()


class Completion(BaseTimestamp):
    """
    Completion model.
    """
    student = models.ForeignKey(User, related_name='completed', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='completed', on_delete=models.CASCADE)
    page = models.ForeignKey(Page, related_name='completed', on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, related_name='completed', on_delete=models.CASCADE, blank=True, null=True)
    assignment = models.ForeignKey(Assignment, related_name='completed', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        # Return student's fullname.
        return f"{self.student.full_name}"