from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from userprofile.models import BaseTimestamp

User = get_user_model()


class Module(BaseTimestamp):
    """
    Module model.
    """
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(User, related_name='courses_modules', on_delete=models.CASCADE)
    course = models.ForeignKey("classroom.Course", related_name='modules', on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        # Return module's title and course's title.
        return f"{self.title} | {self.course.title}"

    def get_add_page_absolute_url(self):
        # Return add page absolute url of course by its slug.
        return reverse("page:add-page", kwargs={"course_slug": self.course.slug, "module_id": self.id})

    def get_add_quiz_absolute_url(self):
        # Return add quiz absolute url of course by its slug.
        return reverse("quiz:add-quiz", kwargs={"course_slug": self.course.slug, "module_id": self.id})   

    def get_add_assignment_absolute_url(self):
        # Return add assignment absolute url of course by its slug.
        return reverse("assignment:add-assignment", kwargs={"course_slug": self.course.slug, "module_id": self.id})           