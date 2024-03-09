from django import forms

class VoteForm(forms.Form):
    recipient_surname = forms.CharField(label='Enter the surname of the student you want to vote for', max_length=50)
