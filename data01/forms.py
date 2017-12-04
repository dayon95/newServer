from django import forms
from data01.models import feedback

class feedbackForm(forms.ModelForm):

    class Meta:
        model = feedback
        fields = ('name', 'message',)
