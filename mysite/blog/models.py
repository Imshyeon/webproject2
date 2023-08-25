from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.db.models import Count

# Create your models here.

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('diary', 'diary'),
        ('travel', 'travel'),
        ('workouts', 'workouts'),
        ('etc', 'etc'),
    ]
    title=models.CharField(max_length=120)
    content=models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='uncategorized')
    likes=models.ManyToManyField(User, related_name="likes",blank=True)
    dislikes = models.ManyToManyField(User, related_name="dislikes",blank=True)
    post_image = models.ImageField(default='default_post_image.jpg',upload_to='post_pics/',null=True,blank=True)
    content_html = models.TextField(editable=False,default='')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk}) #해당 포스트(primary key)로 리버스

    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()

    def save(self, *args, **kwargs):
        self.content_html = markdown.markdown(self.content)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="익명")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    class Meta:
        ordering=["-created_at"]



class ReComment(models.Model):
    replied_to = models.ForeignKey(Comment, related_name="re_comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=255, default="익명2")
    body = models.TextField()
    replied_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.author)

    class Meta:
        ordering = ["-replied_created_at"]