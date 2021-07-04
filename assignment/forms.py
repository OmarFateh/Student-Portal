from django import forms

from .models import Assignment, Submission

from ckeditor.widgets import CKEditorWidget


class AddAssignmentForm(forms.ModelForm):
    """
    Add Assignment model form.
    """
    title = forms.CharField(label='', max_length=150, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'title', 'required': True,})
    )
    content = forms.CharField(widget=CKEditorWidget(), required=True)
    points = forms.IntegerField(max_value=100, min_value=1)
    due = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}), required=True)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model  = Assignment
        fields = ['title', 'content', 'points', 'due', 'files']


class AddSubmissionForm(forms.ModelForm):
    """
    Add Submission model form.
    """
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)
    comment = forms.CharField(label='', 
        widget=forms.Textarea(attrs={'class':'validate', 'placeholder':'Write your comment...', 
            'style': 'width: 100%; resize:none;', 'required': True,
        })
    )

    class Meta:
        model  = Submission
        fields = ['file', 'comment']