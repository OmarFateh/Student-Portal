from django import forms

from .models import Category, Course

from ckeditor.widgets import CKEditorWidget


class AddCourseForm(forms.ModelForm):
    """
    Add Course model form.
    """
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", required=True,
        widget=forms.Select(attrs={'class':"validate select2", 'name':'category', 'style':"width: 100%",'required': True,})
    )
    title = forms.CharField(label='', max_length=150, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'title', 'required': True,})
    )
    description = forms.CharField(label='', required=True,
        widget=forms.Textarea(attrs={'class':'materialize-textarea validate', 'name':'description', 'row':6, 'style':"resize: none;",})
    )
    syllabus = forms.CharField(widget=CKEditorWidget(), required=True)
    photo = forms.ImageField(required=True, )

    class Meta:
        model  = Course
        fields = ['category', 'title', 'description', 'syllabus', 'photo']