from django import forms
from .models import Yatru,Message

class YatruModelForm(forms.ModelForm):
    class Meta:
        model = Yatru
        fields = ('first_name','last_name','bio', 'country','avatar')

class MessageModelForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content','author','receiver')