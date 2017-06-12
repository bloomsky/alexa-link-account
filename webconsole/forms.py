from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='inputEmail3', max_length=32)
    password = forms.CharField(label='inputPassword3', widget=forms.PasswordInput())
