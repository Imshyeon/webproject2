from django import forms
from .models import Comment,ReComment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','category','content']  # category 추가

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = ReComment
        fields=['author','body']