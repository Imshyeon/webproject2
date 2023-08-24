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
    path('', PostListView.as_view(), name="home"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-detail"),
    path('my_posts',views.about, name="posts"),
    path('post/create',PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name="post-edit"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="post-delete"),
    path('post/<int:pk>/add_comment', views.add_comment, name="add-comment"),
    path('post/<int:pk>/add_comment/<int:comment_id>/add_reply', views.add_reply, name="add-reply"),
    path('like/<int:pk>', LikeView, name='like-post'),
    path('dislike/<int:pk>', DisLikeView, name='dislike-post'),
    path('category/<str:category>/', views.get_filtered_posts, name='get_filtered_posts'),
]
