from rest_framework import serializers
from .models import Post, Comment, ReComment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_at', 'author', 'category', 'likes', 'dislikes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'name', 'content', 'created_at']

class ReCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReComment
        fields = ['replied_to', 'author', 'body', 'replied_created_at']


