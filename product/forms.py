from django import forms
from django.core.exceptions import ValidationError

from .models import Comment

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
