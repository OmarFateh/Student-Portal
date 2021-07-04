from django import forms

from .models import Module


class AddModuleForm(forms.ModelForm):
    """
    Add Module model form.
    """
    title = forms.CharField(label='', max_length=150, required=True,
        widget=forms.TextInput(attrs={'class':'validate', 'name':'title', 'required': True,})
    )
    
    class Meta:
        model  = Module
        fields = ['title', 'hours']