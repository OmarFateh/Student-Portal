from django import forms

from .models import Question, Answer

from ckeditor.widgets import CKEditorWidget


class AddQuestionForm(forms.ModelForm):
    """
    Add Question model form.
    """
    title = forms.CharField(label='', max_length=200, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'title', 'required': True,})
    )
    content = forms.CharField(widget=CKEditorWidget(), required=True)

    class Meta:
        model  = Question
        fields = ['title', 'content']


class AddAnswerForm(forms.ModelForm):
    """
    Add Answer model form.
    """
    content = forms.CharField(widget=CKEditorWidget(), required=True)

    class Meta:
        model  = Answer
        fields = ['content']