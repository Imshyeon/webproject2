"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, LikeView, DisLikeView)

urlpatterns = [
    path('', PostListView.as_view(), name="home"),  #홈
    path('post/<int:pk>', PostDetailView.as_view(), name="post-detail"),    #블로그 게시물 싱글
    path('post/create',PostCreateView.as_view(), name='post-create'),   #게시글 작성
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name="post-edit"),   #게시글 편집
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="post-delete"),   #게시글 삭제
    path('post/<int:pk>/add_comment', views.add_comment, name="add-comment"),   #게시글 댓글
    path('post/<int:pk>/add_comment/<int:comment_id>/add_reply', views.add_reply, name="add-reply"),   #게시글 대댓글
    path('like/<int:pk>', LikeView, name='like-post'),   #게시글 좋아요
    path('dislike/<int:pk>', DisLikeView, name='dislike-post'),   #게시글 싫어요
    path('category/<str:category>/', views.get_filtered_posts, name='get_filtered_posts'),   #게시물 카테고리 분류
]
