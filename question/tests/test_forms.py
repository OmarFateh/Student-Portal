import pytest

from question.models import Question, Answer
from question.forms import AddQuestionForm


@pytest.mark.parametrize(
    "title, content, validity",
    [
        ('title test', 'content test', True),
        ('', 'content test', False),
        ('title test', '', False),
    ]
)
def test_add_question_form(title, content, validity):
    """
    Test add question form validation.
    """
    data = {'title': title, 'content': content}
    form = AddQuestionForm(data=data)
    assert form.is_valid() is validity