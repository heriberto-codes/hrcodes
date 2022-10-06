from urllib import request
# from django.shortcuts import render
from django.views.generic import TemplateView
from apps.blog.models import Post


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'base-home.html'
 
    def get_context_data(self, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        print('posts', posts)
        context = {
            'posts': posts,
        }
      
        return context
 