
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
    path('admin_mode/', views.admin_mode_view, name="admin_mode"),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),
         name="password_reset"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name="password_reset_done"),
    path('pw_reset_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),

]