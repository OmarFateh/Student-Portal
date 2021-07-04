from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from userprofile.models import BaseTimestamp
from assignment.models import Submission

from ckeditor.fields import RichTextField

User = get_user_model()


def course_image(instance, filename):
    """
    Upload the course image into the path and return the uploaded image path.
    """
    return f'Courses/{instance.teacher.full_name}/{instance.title}/{filename}'
    
class Category(BaseTimestamp):
    """
    Category model.
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        # Return category's title
        return self.title

    def get_absolute_url(self):
        # Return absolute url of category by its slug.
        return reverse("classroom:category-courses", kwargs={"category_slug": self.slug})


class CourseStudent(BaseTimestamp):
    """
    A relationship model between the course and its students.
    """
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Return course's title
        return f"{self.course.title} | {self.student.full_name}"


class Course(BaseTimestamp):
    """
    Course model.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    teacher = models.ForeignKey(User, related_name='my_courses', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True, through=CourseStudent)
    description = models.TextField()
    syllabus = RichTextField()
    photo = models.ImageField(upload_to=course_image)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return course's title and teacher's full name.
        return f"{self.title} | {self.teacher.full_name}"

    def get_absolute_url(self):
        # Return absolute url of course by its slug.
        return reverse("classroom:course-detail", kwargs={"course_slug": self.slug})

    def get_update_absolute_url(self):
        # Return update absolute url of course by its slug.
        return reverse("classroom:update-course", kwargs={"course_slug": self.slug}) 

    def get_delete_absolute_url(self):
        # Return delete absolute url of course by its slug.
        return reverse("classroom:delete-course", kwargs={"course_slug": self.slug})        

    def get_enroll_absolute_url(self):
        # Return enroll absolute url of course by its slug.
        return reverse("classroom:enroll-course", kwargs={"course_slug": self.slug})

    def get_course_submissions_absolute_url(self): 
        # Return course submissions absolute url of course by its slug.
        return reverse("classroom:course-grades", kwargs={"course_slug": self.slug})

    def get_student_submissions_absolute_url(self):
        # Return student submissions absolute url of course by its slug.
        return reverse("classroom:student-grades", kwargs={"course_slug": self.slug})    

    def get_modules_absolute_url(self):
        # Return modules absolute url of course by its slug.
        return reverse("module:course-modules", kwargs={"course_slug": self.slug})

    def get_add_module_absolute_url(self):
        # Return add module absolute url of course by its slug.
        return reverse("module:add-module", kwargs={"course_slug": self.slug})         
    
    def get_questions_absolute_url(self):
        # Return questions absolute url of course by its slug.
        return reverse("question:course-questions", kwargs={"course_slug": self.slug})

    def get_add_question_absolute_url(self):
        # Return add question absolute url of course by its slug.
        return reverse("question:add-course-question", kwargs={"course_slug": self.slug})    


class Grade(models.Model):
    """
    Grade model.
    """
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Graded', 'Graded'),
    )
    course = models.ForeignKey(Course, related_name='grades', on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, related_name='grades', on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=10)

    def __str__(self):
        # Return course's title, student's full name and grade's points.
        return f"{self.course.title} | {self.submission.student.full_name} | {self.points}"

    def get_absolute_url(self):
        # Return absolute url of grade by its id.
        return reverse("classroom:grade-submission", kwargs={"course_slug": self.course.slug, "grade_id": self.id})     