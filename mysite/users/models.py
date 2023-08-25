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
    follows=models.ManyToManyField("self", related_name="followed_by",symmetrical=False, blank=True)  #symmetrical=False : 내가 팔로우해도 그 사람이 무조건 나를 팔로우 할 필요 없다.
    date_modified = models.DateTimeField(User,auto_now=True)    #프로필 수정한 마지막 날짜

    #음악, 캘린더 api

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


# admin
class AdminModeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_field_1 = models.CharField(max_length=100)
    data_field_2 = models.TextField()
    def __str__(self):
        return f"{self.user.username} - {self.data_field_1}"