from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_manager', '0002_gallerypost_image_main_alter_article_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='excerpt',
            field=models.TextField(),
        ),
    ]
