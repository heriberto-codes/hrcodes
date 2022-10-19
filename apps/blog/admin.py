from django.contrib import admin
from apps.blog.models import Post, Category

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'last_modified', 'status', 'slug')
    list_filter = ('status',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields= ('id',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
