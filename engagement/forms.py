from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, NewsletterSubscriber
from core.profanity import contains_profanity


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content', 'parent']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 text-sm bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-crimson-600 focus:outline-none dark:text-white',
                'placeholder': 'Your Name (optional for guests)'
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 text-sm bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-crimson-600 focus:outline-none dark:text-white',
                'placeholder': 'Your Email (kept private)'
            }),
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-3 text-sm bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-crimson-600 focus:outline-none dark:text-white',
                'placeholder': 'Join the discussion... Share your thoughts respectfully.'
            }),
            'parent': forms.HiddenInput(),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        found, words = contains_profanity(content)
        if found:
            raise ValidationError(
                "Your comment contains inappropriate language. "
                "Please keep the discussion respectful and constructive."
            )
        return content

    def clean_author_name(self):
        name = self.cleaned_data.get('author_name', '')
        found, _ = contains_profanity(name)
        if found:
            raise ValidationError("Please use an appropriate name.")
        return name


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 text-sm bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-l-lg focus:ring-2 focus:ring-crimson-600 focus:outline-none dark:text-white',
                'placeholder': 'Enter your email address'
            })
        }
