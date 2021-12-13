from django.db import models
from ..account.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    image = models.ImageField(upload_to='', null=True, blank=True)
    # likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    # like_count = models.BigIntegerField(default='0')
    public_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'post """{self.title}""" from """{self.author}""" AUTHOR'

class Saved(models.Model):
    user = models.ForeignKey(User, related_name='saved_p', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='saved', on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.saved}'


class Like(models.Model):
    user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='like', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.like}'

# class Like(models.Model):
#     user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
