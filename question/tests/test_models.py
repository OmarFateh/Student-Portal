from django.urls import reverse


## Question
def test_question_str(new_question):
    """
    Test question obj str method.
    """
    assert new_question.__str__() == 'test question | test name'

def test_absolute_url(new_question):
    """
    Test question reverse url response status.
    """
    url = reverse("question:question-detail", kwargs={"course_slug": new_question.course.slug, "question_id": new_question.id})
    assert new_question.get_absolute_url() == url

def test_answers_count_property(db, question_factory, answer_factory):
    """
    Test get answers count property of question.
    """
    question = question_factory.create()
    answer = answer_factory.create()
    assert question.get_answers_count() == 1

## Answer
def test_answer_str(new_answer):
    """
    Test answer obj str method.
    """
    assert new_answer.__str__() == 'test question | test name'

def test_mark_as_answer_absolute_url(new_answer):
    """
    Test mark as answer reverse url response status.
    """
    url = reverse("question:mark-answer", kwargs={"course_slug": new_answer.question.course.slug, 'question_id': new_answer.question.id, "answer_id": new_answer.id})
    assert new_answer.get_mark_as_answer_absolute_url() == url

def test_calculate_votes_property(new_user, answer_factory):
    """
    Test calculate votes property of answer.
    """
    answer = answer_factory.create()
    answer.up_votes.add(new_user)
    assert answer.calculate_votes == 1