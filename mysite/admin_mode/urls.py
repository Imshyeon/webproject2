from django.urls import path
from . import views

urlpatterns = [
    path('admin-mode/', views.admin_mode, name='admin-mode'),

]
