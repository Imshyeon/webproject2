from django import forms
from .models import Comment,ReComment, Post

# choices=Category.objects.all().values_list('name','name')
# choice_list=[]
# for item in choices:
#     choice_list.append(item)
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields=['title','category','content']
#         widgets={
#             'title' : forms.TextInput(attrs={'class':'form-control'}),
#             'category': forms.Select(choices=item,attrs={'class': 'form-control'}),
#             'content': forms.Textarea(attrs={'class': 'form-control'}),
#
#         }

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