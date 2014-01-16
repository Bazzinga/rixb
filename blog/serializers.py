from rest_framework import serializers
from blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('blog_title', 'pub_date', 'short_name')
