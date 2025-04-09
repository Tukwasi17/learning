from django import forms
from .models import Topic, Entry




class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': 'Topic:'}#added label for clarity
        widgets = {'text': forms.TextInput(attrs={'placeholder': 'Enter a topic name'})} #added a placeholder

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        help_texts = {'text': 'Write your entry here.'}# added help text
        widgets = {'text': forms.Textarea(attrs={'cols': 80, 'placeholder': 'Enter your thoughts here.....'})}#added a placeholder