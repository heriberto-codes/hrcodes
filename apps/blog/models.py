from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

# Create a class for Categories 
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=225, unique=False, null=True)
    
    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'slug': self.slug})

# Create a class for Post 
class Post(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(max_length=225, unique=True)
    image = models.ImageField(null=False, blank=False) 
    body = RichTextField(blank=True, null=True)
    snippet = models.CharField(max_length=225, help_text='This text that will show up on the list of blogs page. Write a short snippet of text to describe your blog post.')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', related_name='posts', blank=False)
    status = models.IntegerField(choices=STATUS, default=0)
    
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    
def __str__(self):
    return self.title


#TODO: Create a class for Replies to comments