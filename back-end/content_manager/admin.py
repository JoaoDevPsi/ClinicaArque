# back-end/project_arque/content_manager/admin.py
from django.contrib import admin
from .models import Article, GalleryPost, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image', 'alt_text', 'link', 'order')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    prepopulated_fields = {'id': ('title',)}

@admin.register(GalleryPost)
class GalleryPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_type', 'image_main', 'link', 'created_at') # Adicione 'image_main'
    list_filter = ('post_type',)
    search_fields = ('id', 'link')
    inlines = [GalleryImageInline]
    fieldsets = ( # Organize os campos no admin
        (None, {
            'fields': ('id', 'post_type', 'link', 'image_main') 
        }),
        ('Datas e Metadados', { # Renomeado para clareza
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'id')