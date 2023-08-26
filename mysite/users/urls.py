
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.sign_in,name="login"),
    path('logout/',views.sign_out, name='logout'),
    path('register/',views.sign_up, name="register"),
    path('find_account/',views.change_password, name="find_account"),   #로그인 시 비밀번호 재설정
    path('profile/<int:pk>/edit',views.Myprofile, name='profile'),
    path('profile/<int:pk>',views.profile, name="posts"), # 나의 프로필
    path('admin/', views.admin_mode_view, name="admin_mode"),
]