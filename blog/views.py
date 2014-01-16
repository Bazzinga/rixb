#coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from blog.serializers import *
from blog.models import *


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def show_index(request):
    return render_to_response('index.html')


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly,))
def index_handler(request):
    """
    List latest 6 articles, or post a new article.
    """
    if request.method == 'GET':
        return get_article_list(request)
    elif request.method == 'POST':
        return post_article(request)


def get_article_list(request):
    blog_data = Blog.objects.all()[:6]
    serializer = BlogSerializer(blog_data, many=True)
    return JSONResponse(serializer.data)


def post_article(request):
    serializer = BlogSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data)
    else:
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly,))
def article_handler(request, short_name):
    """
    Get/update/delete a article by `shortName`
    """
    try:
        blog_data = Blog.objects.get(short_name=short_name)
    except Blog.DoesNotExist:
        return JSONResponse(status=status.HTTP_404_NOT_FOUND, data=None)

    if request.method == 'GET':
        return get_article(request, blog_data)
    elif request.method == 'PUT':
        return update_article(request, blog_data)
    elif request.method == 'DELETE':
        return del_article(request, blog_data)


def get_article(request, blog_data):
    blog_data.click += 1
    blog_data.save()
    serializer = BlogSerializer(blog_data)
    return JSONResponse(serializer.data)


def update_article(request, blog_data):
    request.DATA['pub_date'] = timezone.now()
    serializer = BlogSerializer(blog_data, data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data)
    else:
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def del_article(request, blog_data):
    blog_data.delete()
    return JSONResponse(status=status.HTTP_204_NO_CONTENT, data=None)


@api_view(['GET'])
def time_line_handler(request):
    blog_title = Blog.objects.filter(pub_date__year=timezone.now().year)
    serializer = TimelineSerializer(blog_title, many=True)
    return JSONResponse(serializer.data)

