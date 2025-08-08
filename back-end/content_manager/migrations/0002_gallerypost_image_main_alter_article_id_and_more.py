import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallerypost',
            name='image_main',
            field=models.ImageField(blank=True, null=True, upload_to='gallery_main_images/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='gallerypost',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
