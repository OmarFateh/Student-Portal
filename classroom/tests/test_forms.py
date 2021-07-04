import os

from django.conf import settings
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from classroom.models import Category
from classroom.forms import AddCourseForm


class TestClassroomFormValidation(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(title='science', slug='science', icon='science')

    def test_add_course_form(self):
        """
        Test add course form validation.
        """
        upload_file = open(os.path.join(settings.BASE_DIR, 'static/img/no_avatar.jpg'), "rb")
        data = {
            'category': self.category.id,
            'title': 'TEST',
            'description': 'Description',
            'syllabus': 'Syllabus',
        }
        files_data = {
            'photo': SimpleUploadedFile(name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
        }
        form = AddCourseForm(data=data, files=files_data)
        self.assertTrue(form.is_valid())