from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, ReComment
from .forms import CommentForm, ReplyForm, PostForm
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
import markdown

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/home.html', context)

def convert_newlines_to_br(text):
    lines = text.split('\n')
    html_lines = []
    for line in lines:
        html_lines.append(line + '<br>')
    return ''.join(html_lines)

#====================================
class PostListView(ListView):
    model=Post
    template_name = "blog/home.html"   # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ['-published_at']
    def get_context_data(self, *args, **kwargs):
        cat_menu=Post.objects.values_list('category', flat=True).distinct()
        context=super(PostListView,self).get_context_data(*args, **kwargs)

        total_likes = Post.objects.values_list('likes', flat=True).distinct()
        liked=False
        if total_likes.filter(id=self.request.user.id).exists():
            liked=True

        total_dislikes = Post.objects.values_list('dislikes', flat=True).distinct()
        disliked = False
        if total_dislikes.filter(id=self.request.user.id).exists():
            disliked = True

        context['cat_menu']=cat_menu
        context['total_likes'] = total_likes
        context['total_dislikes'] = total_dislikes
        context['liked']=liked
        context['disliked'] = disliked
        return context


def get_filtered_posts(request, category):
    filtered_posts = Post.objects.filter(category=category)
    context = {'filtered_posts': filtered_posts, 'category': category}
    return render(request, 'blog/filtered_posts.html', context)

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        content_html=markdown.markdown(self.object.content)
        context['post'].content=content_html
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # 사용할 폼 지정
    template_name = 'blog/post_form.html'  # 폼을 렌더링할 템플릿 지정

    def form_valid(self, form):
        form.instance.author=self.request.user
        content = form.cleaned_data['content']
        content_html=convert_newlines_to_br(markdown.markdown(content))
        form.instance.content_html=content_html
        return super().form_valid(form)

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author=self.request.user
        content=form.cleaned_data['content']
        content_html=convert_newlines_to_br(markdown.markdown(content))
        form.instance.content_html=content_html
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author: # 현재 로그인한 유저가 포스팅 유저와 같다면..
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'   #삭제하면 홈페이지로 다시 redirect

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

# ============ 댓글 ==============
def add_comment(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form=CommentForm(request.POST, instance=post)
        if form.is_valid():
            name=form.cleaned_data['name']
            content=form.cleaned_data['content']
            comment = Comment(post=post, name=name,content=content,created_at=timezone.now)
            comment.save()
            print(comment.name)
            return redirect('post-detail',pk=pk)
    else :
        form=CommentForm(initial={'name': request.user})
    return render(request,'blog/add_comment.html',{'form':form})

def add_reply(request, pk, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=parent_comment)
        print('is_valid 이전')
        if form.is_valid():
            print('valid')
            author = form.cleaned_data['author']
            body = form.cleaned_data['body']
            re_comment = ReComment(replied_to=parent_comment, author=author, body=body, replied_created_at=timezone.now)
            re_comment.save()
            print(author,'=====',body)
            return redirect('post-detail', pk=parent_comment.post.pk)
    else:
        print('else')
        form = ReplyForm(initial={'author': request.user, 'replied_to': parent_comment})
    return render(request, 'blog/add_reply.html', {'form': form})


#=============================================
def LikeView(request,pk):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))
def DisLikeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        disliked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
