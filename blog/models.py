#coding: utf-8
from django.db import models
from django.utils import timezone


class Blog(models.Model):
    short_name = models.SlugField(max_length=50, unique=True)
    pub_date = models.DateTimeField(default=timezone.now())
    blog_title = models.CharField(max_length=100)
    blog_content = models.TextField()
    click = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.blog_title

    class Meta:
        ordering = ["-id"]