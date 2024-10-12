from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    body = forms.CharField(widget=forms.widgets.Textarea(attrs={"placeholder": "Tweet something now!", "class":"form-control",}), max_length=200, required=True, label="")
    
    class Meta:
        model=Tweet
        exclude = ("user",)