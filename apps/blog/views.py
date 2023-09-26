from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from requests import request
from apps.blog.models import Post, Comment
from .forms import CommentForm

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
        print('post', post)
        print('post', post.__dict__)
        form = CommentForm()
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(
                    author=form.cleaned_data["author"],
                    body=form.cleaned_data["body"],
                    post=post
                )
                comment.save()
                form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        amount_of_comments = len(comments)
        slug = post.slug
        context = {
            'post': post,
            'comments': comments,
            'amount_of_comments': amount_of_comments,
            'slug': slug,
            'form': form,
        }
        
        return render(request, 'blog/blog_detail.html', context)

    except Post.DoesNotExist:
        return render(request, 'blog_detail_error_page.html') 
    
# def like_post(rerquest, post_id):
#     # We get the post and if its not avaiable spit out a 404
#     post = get_object_or_404(Post, id=post_id)
    
#     # if the liked post is not in the current seesion create it 
#     if 'liked_posts' not in request.session:
#         request.session['liked_posts'] = []
       
#     # init a variable to keep track of liked post in the current session     
#     liked_posts = request.session['liked_posts']
    
#     # if the current post id exist in the liked post arra/list 
#     if post_id in liked_posts:
#         # the user already liked the post, so unlike it 
#         liked_posts.remove(post.id)
#     else: 
#         # user hasn't liked the post so like it 
#         liked_posts.append(post_id)
     
#     # inform Django that changes have been made to the session object  
#     request.session.modified = True
    
#     return redirect('blog+detail', slug=post.slug)


#TODO add some color to the blog detail error page and the blog post error page
