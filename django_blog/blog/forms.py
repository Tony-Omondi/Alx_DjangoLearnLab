from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

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
    tags = forms.CharField(max_length=200, required=False, help_text="Enter tags separated by commas")

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        return [tag.strip() for tag in tags.split(',') if tag.strip()]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Handle tags
            tag_names = self.cleaned_data.get('tags', [])
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name.lower())
                tags.append(tag)
            instance.tags.set(tags)
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)