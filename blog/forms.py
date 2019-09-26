from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        
class ContactForm(forms.Form):
	Email = forms.EmailField()
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
