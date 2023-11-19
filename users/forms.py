from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    chat_id = forms.IntegerField(widget=forms.HiddenInput())
