from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from requests import request
from apps.blog.models import Post, Like
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.
def blog_index(request):
    try: 
        posts = Post.objects.all().order_by('-created_on')
        context = {
            'posts': posts,
        }
        return render(request, 'blog/blog_index.html', context)
    
    except Post.DoesNotExist:
        return render(request, 'blog_post_error_page.html')

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts":posts
    }
    return render(request, 'blog/blog_category.html', context)

#TODO use local stoarge to manage likes, use a variable to keep track of how many likes 
def blog_detail(request, pk, slug):
    try:
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(post=post)
        slug = post.slug
        post_was_liked = 'liked' in request.GET and request.GET['liked'] == 'true'
        
        context = {
            'post': post,
            'slug': slug,
            'like': like,
            'post_was_liked': post_was_liked
        }
        
        return render(request, 'blog/blog_detail.html', context)

    except Like.DoesNotExist:
        return render(request, 'blog_detail_error_page.html')
    
    except Post.DoesNotExist:
        return render(request, 'blog_detail_error_page.html') 


def like_post(request, pk, slug):
    # get the post by id 
    post = get_object_or_404(Post, pk=pk)
    # get the set of liked post from the session or create an empty set 
    liked_posts = list(request.session.get('liked_posts', set()))
    # check if the post has already been liked in the current session 
    if post.pk not in liked_posts:
        # if not liked, create a like instance and increment the like 
        liked, created = Like.objects.get_or_create(post=post) 
        liked.increment_likes()
        # add the post to the set of liked posts in the session 
        liked_posts.append(post.pk)
        request.session['liked_posts'] = liked_posts

    # return HttpResponseRedirect(reverse('blog_detail', args=[pk, slug]))
    return HttpResponseRedirect(reverse('blog_detail', args=[pk, slug]) + '?liked=true')

#TODO add some color to the blog detail error page and the blog post error page
