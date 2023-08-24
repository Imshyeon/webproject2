from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, ReComment
from .forms import CommentForm, ReplyForm, PostForm
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


def about(request):
    # posts=Post.objects.all()
    # context = {'posts' : posts}
    return render(request, 'blog/me_profile.html')

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/home.html', context)

#====================================
class PostListView(ListView):
    model=Post
    template_name = "blog/home.html"   # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ['-published_at']

class PostDetailView(DetailView):
    model = Post

    # def get_context_data(self, *args, **kwargs):
    #     # context['total_likes'] = total_likes
    #     pass

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title','category','content']
#     # form_class = PostForm
#
#     def form_valid(self, form): #Post 눌렀을 때 제대로 올라가기 위해서..
#         form.instance.author = self.request.user    #쓰는사람 현재 유저야!
#         return super().form_valid(form) #부모 클래스로 전달
#     # 이것만 하면 define a get_absolute_url method on the Model. 오류 발생 -> Model.py


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # 사용할 폼 지정
    template_name = 'blog/post_form.html'  # 폼을 렌더링할 템플릿 지정

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','category','content']


    def form_valid(self, form):
        form.instance.author = self.request.user
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
            return redirect('post-detail',pk=pk)
    else :
        form=CommentForm()
    return render(request,'blog/add_comment.html',{'form':form})

def add_reply(request, pk, comment_id):
    print("add_reply view called with pk:", pk, "and comment_id:", comment_id)
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=parent_comment)
        if form.is_valid():
            re_comment = form.save(commit=False)
            re_comment.replied_to = parent_comment
            re_comment.replied_created_at = timezone.now()
            re_comment.save()
            print(form)
            return redirect('post-detail', pk=parent_comment.post.pk)
    else:
        form = ReplyForm()  # 유효하지 않은 폼의 경우 폼 객체를 다시 생성해야 함
    return render(request, 'blog/add_reply.html', {'form': form})

#=============================================
def LikeView(request,pk):
    post=get_object_or_404(Post,id=request.POST.get('post_id')) #likes?
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))
