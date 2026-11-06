from django.contrib import admin
from apps.blog.models import Post, Category, Like

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'last_modified', 'status', 'slug')
    list_filter = ('status',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields= ('id',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        # Body and snippets assume trusted authors. Before broadening input to
        # less-trusted authors, imports, or visitors, require server-side HTML
        # sanitization and explicit allowed URL schemes at every rendered sink.
        guidance = {
            'body': 'The article body is rendered as trusted HTML.',
            'snippet': 'The snippet is rendered as trusted HTML.',
        }
        if formfield is not None and db_field.name in guidance:
            help_text = (
                f'{guidance[db_field.name]} Review pasted markup and link '
                'destinations before saving. Restrict post add/change '
                'permissions to trusted site authors.'
            )
            formfield.help_text = ' '.join(
                text for text in (formfield.help_text, help_text) if text
            )
        return formfield

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    

class LikeAdmin(admin.ModelAdmin):
    list_post = ('post')
    list_like = ('like')
    

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Like, LikeAdmin)
