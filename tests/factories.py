from django.contrib.auth import get_user_model

from classroom.models import Category, Course
from module.models import Module
from question.models import Question, Answer

import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Create new user instance.
    """
    class Meta:
        model = User
        django_get_or_create = ('email',)

    full_name = 'test name'
    email = 'testemail@gmail.com'
    password = 'admin1600'
    is_active = True


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Create new category instance.
    """
    class Meta:
        model = Category
        django_get_or_create = ('slug',)

    title = 'science' 
    slug = 'science'
    icon = 'science'


class CourseFactory(factory.django.DjangoModelFactory):
    """
    Create new course instance.
    """
    class Meta:
        model = Course
        django_get_or_create = ('slug',)

    title = 'physics'
    slug = 'physics'
    teacher = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    description = 'description'
    syllabus = 'syllabus'


class ModuleFactory(factory.django.DjangoModelFactory):
    """
    Create new module instance.
    """
    class Meta:
        model = Module
        
    title = 'introduction'
    teacher = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    hours = '5'


class QuestionFactory(factory.django.DjangoModelFactory):
    """
    Create new module instance.
    """
    class Meta:
        model = Question
        django_get_or_create = ('title',)

    title = 'test question'
    content = 'test question content'
    student = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    has_accepted_answer = False


class AnswerFactory(factory.django.DjangoModelFactory):
    """
    Create new module instance.
    """
    class Meta:
        model = Answer

    student = factory.SubFactory(UserFactory)
    question = factory.SubFactory(QuestionFactory)
    content = 'test answer content'
    is_accepted_answer = False

    @factory.post_generation
    def up_votes(self, create, extracted, **kwargs):
        if not create:
            AnswerFactory.build()
            return

        if extracted:
            print(extracted)
            # A list of user were passed in, use them
            for user in extracted:
                self.up_votes.add(user)
    
    # up_votes = models.ManyToManyField(User, related_name='up_votes_answers', blank=True)
    # down_votes = models.ManyToManyField(User, related_name='down_votes_answers', blank=True)
    # votes = models.IntegerField(default=0)   