from django import forms
from .models import Post

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('no_people','no_days','tour_date', 'Gender_prefer','location','detail','author')