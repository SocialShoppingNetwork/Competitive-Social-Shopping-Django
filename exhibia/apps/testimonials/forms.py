from django import forms

class ReviewForm(forms.Form):
    rated = forms.IntegerField(max_value=5, min_value=1, initial=0)
    review = forms.CharField(widget=forms.Textarea())
    video = forms.FileField()

    share_twitter = forms.BooleanField(initial=False)
    share_facebook = forms.BooleanField(initial=False)