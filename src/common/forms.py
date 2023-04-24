from django import forms

class CommentForm(forms.Form):
    description = forms.CharField(max_length=512, required=True)

