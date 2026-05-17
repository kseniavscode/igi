from django import forms
from .models import Review, FAQ


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control', 'placeholder': 'Mark'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your review...', 'rows': 3}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ask your question...'}),
        }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write an answer...'}),
        }