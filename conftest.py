import pytest
from pytest_factoryboy import register

from tests.factories import (
    UserFactory, CategoryFactory, CourseFactory, ModuleFactory, QuestionFactory, AnswerFactory
)

register(UserFactory)
register(CategoryFactory)
register(CourseFactory)
register(ModuleFactory)
register(QuestionFactory)
register(AnswerFactory)


@pytest.fixture
def new_user(db, user_factory, client):
    user = user_factory.create()
    client.force_login(user)
    return user

# @pytest.fixture
# def new_category(db, category_factory):
#     category = category_factory.create()
#     return category

@pytest.fixture
def new_course(db, course_factory):
    course = course_factory.create()
    return course

@pytest.fixture
def new_module(db, module_factory):
    module = module_factory.create()
    return module

@pytest.fixture
def new_question(db, question_factory):
    question = question_factory.create()
    return question

@pytest.fixture
def new_answer(db, answer_factory):
    answer = answer_factory.create()
    return answer           