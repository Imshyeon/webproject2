
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ProfileAPI

urlpatterns = [
    path('login/',views.sign_in,name="login"),
    path('logout/',views.sign_out, name='logout'),
    path('register/',views.sign_up, name="register"),
    path('find_account/',views.change_password, name="find_account"),   #로그인 시 비밀번호 재설정

    path('pw_reset/',auth_views.PasswordResetView.as_view(),name="pw_reset"),

    path('profile/',views.Myprofile, name='profile'),
# =====================API===================================================
    path('api/profile/', views.ProfileAPI.as_view(), name='profile-api'),

]