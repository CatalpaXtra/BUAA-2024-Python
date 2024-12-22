from django import forms


class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=2)
    content = forms.CharField()
    category = forms.IntegerField()