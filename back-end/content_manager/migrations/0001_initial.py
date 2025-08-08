import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('excerpt', models.TextField(max_length=300)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='articles/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GalleryPost',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('post_type', models.CharField(choices=[('single', 'Imagem Única'), ('carousel', 'Carrossel')], max_length=10)),
                ('link', models.URLField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery/')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True)),
                ('link', models.URLField(blank=True, max_length=500, null=True)),
                ('order', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='content_manager.gallerypost')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('post', 'order')},
            },
        ),
    ]
