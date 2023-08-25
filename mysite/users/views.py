from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .forms import LoginForm, RegisterForm, ChangePW, ResetPW, ProfileImageForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.core.files import File
from io import BytesIO
# =====================API============================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer



# Create your views here.

def home(request):
    return render(request, 'users/home.html')


# =========================== login / logout ===========================
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
                return render(request, 'users/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f"You've been logged out")
    return redirect('login')


# =========================== 회원등록 ===========================
def sign_up(request, false=None):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register2.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=false)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You've signed up successfully")
            login(request, user)  # signup에 성공하면 그것을 이용해서 바로 로그인
            return redirect('posts')
        else:
            return render(request, 'users/register2.html', {'form': form})


# =========================== 계정 찾기 ===========================
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePW(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "You're password changed successfully")
            return redirect('login')
    else:
        form = ChangePW(request.user)
    return render(request, 'users/changePW.html', {'form': form})


# def pw_reset(request):
#     if request.method=='POST':
#         form = PasswordResetForm(request.POST or None)
#         if form.is_valid():
#             form.save(
#                 template_name='users/password_reset_form.html',
#                 subject_template_name='users/password_reset_subject.txt',
#                 email_template_name='users/password_reset_email.html',
#                 request=request,
#                 use_https=request.is_secure(),
#             )
#             messages.success(request,'이메일에 링크를 성공적으로 보냈습니다.')
#             return redirect('login')
#     else:
#         form = PasswordResetForm(request)
#     return render(request,'users/password_reset_form.html',{'form':form})

# ========================== 프로필 =============================
@login_required
def Myprofile(request):
    user_profile = request.user.profile
    if request.method == 'GET':
        form = ProfileImageForm(instance=user_profile)
        return render(request, 'users/profile.html', {'form': form})
    elif request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            image = form.cleaned_data['image']
            img = Image.open(image)
            img = img.resize((200, 200), Image.LANCZOS)
            image_io = BytesIO()
            img.save(image_io, format='JPEG')
            edited_img = File(image_io, name=image.name)
            form.cleaned_data['image'] = edited_img
            form.save()
            return redirect('posts')
    else:
        form = ProfileImageForm(instance=user_profile)
    return render(request, 'users/profile.html', {'form': form})


# =====================API===================================================
class ProfileAPI(APIView):
    def get(self, request, format=None):
        user_profile = request.user.profile
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        user_profile = request.user.profile
        serializer = ProfileSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# admin_mode =================
