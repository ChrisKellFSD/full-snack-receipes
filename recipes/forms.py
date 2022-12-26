from .models import Comment, Recipe
from django_summernote.widgets import SummernoteWidget
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title', 'excerpt', 'ingredients', 'method',
            'featured_image', 'status'
            )
        # SummernoteWidget learned from https://github.com/summernote/django-summernote
        # and also https://summernote.org/deep-dive/
        widgets = {
            'excerpt': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
            'method': SummernoteWidget(),
        }