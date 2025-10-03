from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagField
from .models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class PostForm(forms.ModelForm):
    tags = TagField(required=False, help_text="Enter tags separated by commas")

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)