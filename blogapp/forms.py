from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import BlogModel, CommentModel, User

class LoginForm(forms.Form):
    email = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class RegisterForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    home_address = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'age', 'state', 'home_address', 'password1', 'password2')

    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data.get('age')
        if not age == 0:
            return age
        else:
            raise forms.ValidationError('Kindly select age range')

    def clean_state(self, *args, **kwargs):
        state = self.cleaned_data.get('state')
        if not state == 0:
            return state
        else:
            raise forms.ValidationError('Kindly select state')

class PostForm(forms.ModelForm):

    class Meta:
        model = BlogModel
        fields = ['blog_title','blog']
        labels = {}

class CommentForm(forms.ModelForm):
    class Meta:
        model= CommentModel
        fields = ['comment_text']
        labels = {}
 
    def __str__(self):
        return f"{self.comment_text}"
 
class SearchForm(forms.Form):
    title = forms.CharField(max_length=200)