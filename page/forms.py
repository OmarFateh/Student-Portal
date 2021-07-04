from django import forms

from .models import Page

from ckeditor.widgets import CKEditorWidget


class AddPageForm(forms.ModelForm):
    """
    Add Page model form.
    """
    title = forms.CharField(label='', max_length=150, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'title', 'required': True,})
    )
    content = forms.CharField(widget=CKEditorWidget(), required=True)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model  = Page
        fields = ['title', 'content', 'files']