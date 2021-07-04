import os

from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from classroom.models import Category, CourseStudent, Course, Grade
from module.models import Module
from assignment.models import Assignment, Submission

User = get_user_model()


class TestModel(TestCase):

    def setUp(self):
        """
        Create new instances objects of every model for testing.
        """
        self.category = Category.objects.create(title='science', slug='science', icon='science')
        self.user = User.objects.create(email='admin@gmail.com', full_name='admin')
        # course
        upload_file = open(os.path.join(settings.BASE_DIR, 'static/img/no_avatar.jpg'), "rb")
        photo = SimpleUploadedFile(name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
        self.course = Course.objects.create(title='physics', slug='physics', teacher_id=1, category_id=1, 
                                description='description', syllabus='syllabus', photo=photo)  
        # course student
        self.course_student = CourseStudent.objects.create(course_id=1, student_id=1)
        # grade
        Module.objects.create(title='introduction', teacher_id=1, course_id=1, hours=5)
        Assignment.objects.create(title='assignment', content='content', points=20, due='2021-06-23', 
                                    teacher_id=1, module_id=1)
        Submission.objects.create(student_id=1, assignment_id=1, comment='comment')                        
        self.grade = Grade.objects.create(course_id=1, submission_id=1, points=5, status='Pending')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes.
        """
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), 'science')
        self.assertEqual(self.category.get_absolute_url(), '/courses/categories/science/')

    def test_course_student_model_entry(self):
        """
        Test CourseStudent model data insertion/types/field attributes.
        """
        self.assertTrue(isinstance(self.course_student, CourseStudent))
        self.assertEqual(str(self.course_student), 'physics | admin')
    
    def test_course_model_entry(self):
        """
        Test Course model data insertion/types/field attributes.
        """
        self.assertTrue(isinstance(self.course, Course))
        self.assertEqual(str(self.course), 'physics | admin')

    def test_course_image_path(self):
        """
        Test course image upload path.
        """
        upload_file = open(os.path.join(settings.BASE_DIR, 'static/img/no_avatar.jpg'), "rb")
        photo = SimpleUploadedFile(name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
        course = Course.objects.create(title='physics1', slug='physics1', teacher_id=1, category_id=1, 
                                description='description', syllabus='syllabus', photo=photo)  
        photo_name = course.photo.name.split('/')[-1]
        photo_path = os.path.join(settings.BASE_DIR, f'media\\Courses\\admin\\physics1\\{photo_name}')
        self.assertEqual(course.photo.path, photo_path)

    def test_grade_model_entry(self):
        """
        Test Grade model data insertion/types/field attributes.
        """
        self.assertTrue(isinstance(self.grade, Grade))
        self.assertEqual(str(self.grade), 'physics | admin | 5')