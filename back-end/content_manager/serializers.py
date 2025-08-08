import json
from rest_framework import serializers
from .models import Article, GalleryPost, GalleryImage
from contact_form.models import ContactSubmission

class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False, allow_null=True)

    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'alt_text', 'link', 'order']
        read_only_fields = ['id']

class GalleryPostSerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, required=False)

    class Meta:
        model = GalleryPost
        fields = ['id', 'post_type', 'link', 'image_main', 'images', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        validated_data.pop('images', None) 
        
        images_meta_str = self.context['request'].data.get('images_meta', '[]')
        images_meta = json.loads(images_meta_str) if isinstance(images_meta_str, str) else images_meta_str
        
        image_main_file = self.context['request'].FILES.get('image_main')
        image_main_url = validated_data.get('image_main') 

        gallery_post = GalleryPost.objects.create(
            post_type=validated_data['post_type'],
            link=validated_data.get('link'),
            image_main=image_main_file or image_main_url
        )

        if gallery_post.post_type == 'carousel':
            for idx, img_meta in enumerate(images_meta):
                image_file_key = f'images_files[{idx}]'
                image_file = self.context['request'].FILES.get(image_file_key)
                
                image_to_use = None
                if image_file:
                    image_to_use = image_file
                elif 'image' in img_meta and img_meta['image'] and not img_meta['image'].startswith('blob:'):
                    image_to_use = img_meta['image']

                if image_to_use:
                    GalleryImage.objects.create(
                        post=gallery_post,
                        image=image_to_use,
                        alt_text=img_meta.get('alt_text', ''),
                        link=img_meta.get('link', ''),
                        order=img_meta.get('order', idx)
                    )
        return gallery_post

    def update(self, instance, validated_data):
        instance.post_type = validated_data.get('post_type', instance.post_type)
        instance.link = validated_data.get('link', instance.link)

        new_image_file = self.context['request'].FILES.get('image_main')
        new_image_url = validated_data.get('image_main') 

        if new_image_file:
            instance.image_main = new_image_file
        elif new_image_url and not new_image_url.startswith('blob:'):
            instance.image_main = new_image_url
        elif 'image_main' in self.context['request'].data and not self.context['request'].data['image_main']:
            instance.image_main = None

        instance.save()
        
        validated_data.pop('images', None)

        if instance.post_type == 'carousel':
            instance.images.all().delete()

            images_meta_str = self.context['request'].data.get('images_meta', '[]')
            images_meta = json.loads(images_meta_str) if isinstance(images_meta_str, str) else images_meta_str
            
            for idx, img_meta in enumerate(images_meta):
                image_file_key = f'images_files[{idx}]'
                image_file = self.context['request'].FILES.get(image_file_key)
                
                image_to_use = None
                if image_file:
                    image_to_use = image_file
                elif 'image' in img_meta and img_meta['image'] and not img_meta['image'].startswith('blob:'):
                    image_to_use = img_meta['image']

                if image_to_use:
                    GalleryImage.objects.create(
                        post=instance,
                        image=image_to_use,
                        alt_text=img_meta.get('alt_text', ''),
                        link=img_meta.get('link', ''),
                        order=idx
                    )
        return instance


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'excerpt', 'content', 'image', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.excerpt = validated_data.get('excerpt', instance.excerpt)
        instance.content = validated_data.get('content', instance.content)

        new_image_file = self.context['request'].FILES.get('image')
        new_image_url = validated_data.get('image')

        if new_image_file:
            instance.image = new_image_file
        elif new_image_url:
            instance.image = new_image_url
        elif 'image' in self.context['request'].data and not self.context['request'].data['image']:
            instance.image = None
        
        instance.save()
        return instance

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'phone', 'message', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']
