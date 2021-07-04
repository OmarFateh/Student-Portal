from django.urls import reverse
from django.contrib.auth import get_user_model

from question.models import Answer

import pytest

User = get_user_model()


def test_add_course_question_func(client, new_user, new_course):
    """
    Test add course question response status.
    """
    # Get data
    response = client.get(new_course.get_add_question_absolute_url())
    assert response.status_code == 200
    # post data
    assert new_course.questions.count() == 0
    data = {'title': 'title test', 'content': 'content test'}
    response = client.post(new_course.get_add_question_absolute_url(), data=data)
    assert new_course.questions.count() == 1
    assert response.status_code == 302 and response.url == new_course.get_questions_absolute_url()

def test_course_questions_func(client, new_user, new_course):
    """
    Test course questions response status.
    """
    response = client.get(new_course.get_questions_absolute_url())
    assert response.status_code == 200

def test_question_detail_func(client, new_user, new_course, new_question):
    """
    Test question detail response status.
    """
    # Get data
    response = client.get(new_question.get_absolute_url())
    assert response.status_code == 200
    # Add answer
    assert new_question.answers.count() == 0
    data = {'content': 'content test'}
    response = client.post(new_question.get_absolute_url(), data=data)
    assert new_question.answers.count() == 1
    assert response.status_code == 302 and response.url == new_question.get_absolute_url()

def test_mark_as_answer_func(client, new_user, new_course, new_question, new_answer):
    """
    Test mark as answer response status.
    """
    assert new_answer.is_accepted_answer is False
    assert new_question.has_accepted_answer is False
    response = client.get(new_answer.get_mark_as_answer_absolute_url())
    new_answer.refresh_from_db()
    new_question.refresh_from_db()
    assert new_answer.is_accepted_answer is True
    assert new_question.has_accepted_answer is True
    assert response.status_code == 302 and response.url == new_question.get_absolute_url()

def test_vote_answer_func(client, new_user, new_course, new_question, new_answer):
    """
    Test vote answer response status.
    """
    data = {'answer_id': new_answer.id, 'vote_type': 'U'}
    url = reverse('question:vote-answer', kwargs={'course_slug': new_course.slug, 'question_id': new_question.id})
    # up vote
    new_answer.down_votes.add(new_user)
    response = client.post(url, data=data)
    assert new_user not in new_answer.down_votes.all()
    assert new_answer.calculate_votes == 1
    assert response.status_code == 200
    # down vote
    data['vote_type'] = 'D'
    response = client.post(url, data=data)
    assert new_answer.calculate_votes == -1
    assert response.status_code == 200
    # test exception, answer_id doesn't exist
    data['answer_id'] = 2
    with pytest.raises(Exception) as e:
        response = client.post(url, data=data)    
    assert e.type == Answer.DoesNotExist

def test_course_teacher_nor_student_forbid(client, new_user, new_course, new_question, new_answer):
    """
    Test course teacher or course student forbidden response status.
    User is not the teacher nor a student of this course
    """
    # create new user and login this user
    user = User.objects.create_user(email='admin1@gmail.com', password='test1600', is_active=True)
    client.force_login(user)
    # add course question
    add_question_response = client.get(new_course.get_add_question_absolute_url())
    assert add_question_response.status_code == 403
    # question_detail
    question_response = client.get(new_question.get_absolute_url())
    assert question_response.status_code == 403
    # mark as answer
    mark_as_answer_response = client.get(new_answer.get_mark_as_answer_absolute_url())
    assert mark_as_answer_response.status_code == 403
    # vote answer
    vote_answer_response = client.get(reverse('question:vote-answer', kwargs={'course_slug': new_course.slug, 'question_id': new_question.id}))
    assert vote_answer_response.status_code == 403