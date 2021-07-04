from django import forms

from .models import Quiz, QuizQuestion, QuizAnswer

from ckeditor.widgets import CKEditorWidget


class AddQuizForm(forms.ModelForm):
    """
    Add Quiz model form.
    """
    title = forms.CharField(label='', max_length=150, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'title', 'required': True,})
    )
    description = forms.CharField(widget=CKEditorWidget(), required=True)
    due = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}), required=True)
    allowed_attempts = forms.IntegerField(max_value=100, min_value=1)
    time_limit_mins = forms.IntegerField(max_value=360, min_value=1)

    class Meta:
        model  = Quiz
        fields = ['title', 'description', 'due', 'allowed_attempts', 'time_limit_mins']


class AddQuizQuestionForm(forms.ModelForm):
    """
    Add Quiz Question model form.
    """
    question_text = forms.CharField(label='', max_length=800, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'question', 'required': True,})
    )
    points = forms.IntegerField(max_value=100, min_value=1)

    class Meta:
        model  = QuizQuestion
        fields = ['question_text', 'points']


class AddQuizAnswerForm(forms.ModelForm):
    """
    Add Quiz Answer model form.
    """
    answer_text = forms.CharField(label='', max_length=800, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'answer', 'required': True,})
    )
    is_correct = forms.BooleanField(required=True)

    class Meta:
        model  = QuizAnswer
        fields = ['answer_text', 'is_correct']