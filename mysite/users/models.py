from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
#Pillow 설치 필요 : 이미지 사용을 위해
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)   # 유저는 하나의 프로필을 가질 수 있다. 1:1
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')   #>>> user.profile.image.url # '/media/profile_pics/django.png'
    nickname = models.CharField(max_length=60, default='default_nickname')
    self_introduce = models.TextField(default='Hello world!')
    #음악, 캘린더 api

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

# admin_mode------------------------------------시작
