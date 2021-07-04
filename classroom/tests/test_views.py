import os

from django.conf import settings
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from classroom.models import Category, CourseStudent, Course, Grade
from module.models import Module
from assignment.models import Assignment, Submission
from classroom.views import (
    categories, 
    category_courses, 
    course_detail, 
    add_course, 
    update_course, 
    delete_course,
    my_courses, 
    enroll_course, 
    course_grades, 
    student_grades, 
    grade_submission
)

User = get_user_model()


class TestClassroomViewResponses(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        # category 
        self.category = Category.objects.create(title='science', slug='science', icon='science')
        # user
        self.user = User.objects.create_user(email='admin@gmail.com', password='admin', is_active=True)
        self.c.force_login(self.user)
        # course
        upload_file = open(os.path.join(settings.BASE_DIR, 'static/img/no_avatar.jpg'), "rb")
        self.photo = SimpleUploadedFile(name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
        self.course = Course.objects.create(title='physics', slug='physics', teacher_id=1, category_id=1, 
                                description='description', syllabus='syllabus', photo=self.photo)
        # grade
        Module.objects.create(title='introduction', teacher_id=1, course_id=1, hours=5)
        Assignment.objects.create(title='assignment', content='content', points=20, due='2021-06-23', 
                                    teacher_id=1, module_id=1)
        Submission.objects.create(student_id=1, assignment_id=1, file=self.photo, comment='comment')
        self.grade = Grade.objects.create(course_id=1, submission_id=1, points=5, status='Pending')                        
         
    def test_categories_html(self):
        """
        Test categories response status.
        """
        request = HttpRequest()
        response = categories(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Categories</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_category_courses_func(self):
        """
        Test category courses response status.
        """
        request = self.factory.get(self.category.get_absolute_url())
        response = category_courses(request, self.category.slug)
        html = response.content.decode('utf8')
        self.assertIn(f'<title>{self.category.title.title()}</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_func(self):
        """
        Test course detail response status.
        """
        request = self.factory.get(self.course.get_absolute_url())
        request.user = self.user
        response = course_detail(request, self.course.slug)
        html = response.content.decode('utf8')
        self.assertIn(f'<title>{self.course.title.title()}</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_add_course_func(self):
        """
        Test add course response status.
        """
        # Get data
        request = self.factory.get(reverse("classroom:add-course"))
        request.user = self.user
        response = add_course(request)
        self.assertEqual(response.status_code, 200)
        # Post data
        request = self.factory.post(reverse("classroom:add-course"))
        request.user = self.user
        response = add_course(request)
        self.assertEqual(response.status_code, 200)

    def test_add_course_post_data(self):
        """
        Test add course post data response status.
        """
        # add course
        upload_file = open(os.path.join(settings.BASE_DIR, 'static/img/no_avatar.jpg'), "rb")
        data = {
            'category': self.category.id,
            'title': 'TEST',
            'description': 'Description',
            'syllabus': 'Syllabus',
            'photo': SimpleUploadedFile(name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
        }
        request = self.factory.post(reverse("classroom:add-course"), data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        response = add_course(request)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course_func(self):
        """
        Test update course response status.
        """
        # Get data
        response = self.c.get(self.course.get_update_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/update_course.html')
        # Post data
        self.assertEqual(self.course.title, 'physics')
        data = {
            'category': 1,
            'title': 'Title',
            'description': 'Description1',
            'syllabus': 'Syllabus1',
        }
        files_data = {'photo': self.photo}
        response = self.c.post(self.course.get_update_absolute_url(), data=data, files=files_data)
        self.course.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.title, 'Title')
        self.assertEqual(self.course.description, 'Description1')
        self.assertEqual(self.course.syllabus, 'Syllabus1')

    def test_delete_course_func(self):
        """
        Test delete course response status.
        User is the teacher of this course.
        """
        request = self.factory.get(self.course.get_delete_absolute_url())
        request.user = self.user
        delete_course(request, self.course.slug)
        self.assertEqual(Course.objects.count(), 0)

    def test_my_courses_func(self):
        """
        Test my courses response status.
        """
        response = self.c.get(reverse("classroom:my-courses"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/my_courses.html')

    def test_enroll_course_func(self):
        """
        Test enroll course response status.
        Test student grades response status when User is enrolled in this course.
        """
        request = self.factory.get(self.course.get_enroll_absolute_url())
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        enroll_course(request, self.course.slug)
        self.assertEqual(self.course.students.count(), 1)
        # test student grade func
        response = self.c.get(self.course.get_student_submissions_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/student_grades.html')

    def test_course_grades_func(self):
        """
        Test course grades response status.
        """
        response = self.c.get(self.course.get_course_submissions_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/course_grades.html')

    def test_grade_submission_func(self):
        """
        Test grade submission response status.
        """
        response = self.c.get(self.grade.get_absolute_url())
        self.assertTemplateUsed(response, 'classroom/grade_submission.html')
        # post data
        data = {'points': 10}
        self.assertEqual(self.grade.points, 5)
        request = self.c.post(self.grade.get_absolute_url(), data=data)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.points, 10)

    def test_course_teacher_forbid(self):
        """
        Test course teacher forbidden response status.
        User is not the teacher of this course.
        """
        # create new user and login this user
        new_user = User.objects.create_user(email='admin1@gmail.com', password='admin', is_active=True)
        self.c.force_login(new_user)
        # update course
        update_response = self.c.get(self.course.get_update_absolute_url())
        self.assertEqual(update_response.status_code, 403)
        # delete course
        delete_response = self.c.get(self.course.get_delete_absolute_url())
        self.assertEqual(delete_response.status_code, 403)
        # course grades
        course_grades_response = self.c.get(self.course.get_course_submissions_absolute_url())
        self.assertEqual(course_grades_response.status_code, 403)
        # grade submission
        grade_submission_response = self.c.get(self.grade.get_absolute_url())
        self.assertEqual(grade_submission_response.status_code, 403)

    def test_course_student_forbid(self):
        """
        Test course student forbidden response status.
        User is not enrolled in this course.
        """
        # student grades
        response = self.c.get(self.course.get_student_submissions_absolute_url())
        self.assertEqual(response.status_code, 403)   