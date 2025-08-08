from django.db import models
import uuid

class Article(models.Model):
    id = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class GalleryPost(models.Model):
    id = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    post_type = models.CharField(max_length=10, choices=[('single', 'Imagem Única'), ('carousel', 'Carrossel')])
    link = models.URLField(max_length=500, blank=True, null=True)
    image_main = models.ImageField(upload_to='gallery_main_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gallery Post ({self.post_type}) - {self.id}"

    class Meta:
        ordering = ['-created_at']

class GalleryImage(models.Model):
    post = models.ForeignKey(GalleryPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Image for {self.post.id} - {self.order}"

    class Meta:
        ordering = ['order']
        unique_together = ('post', 'order')