from django import forms
from django.utils.translation import gettext as _

class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'placeholder': _('First name')}),
        label='First name'
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': _('Last name')}), 
        label='Last name'
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
