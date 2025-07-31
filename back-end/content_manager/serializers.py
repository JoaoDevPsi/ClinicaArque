# back-end/project_arque/content_manager/serializers.py
import json
from rest_framework import serializers
from .models import Article, GalleryPost, GalleryImage

class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = GalleryImage
        fields = ['image', 'alt_text', 'link', 'order']

class GalleryPostSerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = GalleryPost
        # Adicione 'image_main' aos fields que o serializer deve lidar
        fields = ['id', 'post_type', 'link', 'image_main', 'images', 'created_at', 'updated_at']
        read_only_fields = ['images', 'created_at', 'updated_at']

    def create(self, validated_data):
        images_meta_str = self.context['request'].data.get('images_meta', '[]')
        images_meta = json.loads(images_meta_str) if isinstance(images_meta_str, str) else images_meta_str

        # --- Lógica para image_main para tipo 'single' ---
        # O arquivo 'image' para posts single vem diretamente no request.FILES
        image_main_file = self.context['request'].FILES.get('image') 
        # O valor do campo 'image' pode ser uma URL se o usuário colou
        image_main_url_from_data = validated_data.get('image')

        gallery_post = GalleryPost.objects.create(
            id=validated_data.get('id', None),
            post_type=validated_data['post_type'],
            link=validated_data.get('link'),
            # Salva a imagem principal: prioriza o arquivo, senão a URL (se existir e não for blob:)
            image_main=image_main_file if image_main_file else (image_main_url_from_data if image_main_url_from_data and not image_main_url_from_data.startswith('blob:') else None)
        )

        # Processa e cria GalleryImages APENAS se for carrossel
        if gallery_post.post_type == 'carousel':
            for idx, img_meta in enumerate(images_meta):
                image_file_key = f'images_files[{idx}]'
                image_file = self.context['request'].FILES.get(image_file_key)

                if image_file:
                    GalleryImage.objects.create(
                        post=gallery_post,
                        image=image_file,
                        alt_text=img_meta.get('alt_text', ''),
                        link=img_meta.get('link', ''),
                        order=img_meta.get('order', idx)
                    )
                elif 'image' in img_meta and img_meta['image'] and not img_meta['image'].startswith('blob:'):
                    GalleryImage.objects.create(
                        post=gallery_post,
                        image=img_meta['image'],
                        alt_text=img_meta.get('alt_text', ''),
                        link=img_meta.get('link', ''),
                        order=img_meta.get('order', idx)
                    )
        return gallery_post

    def update(self, instance, validated_data):
        instance.post_type = validated_data.get('post_type', instance.post_type)
        instance.link = validated_data.get('link', instance.link)

        # --- Lógica de atualização para image_main ---
        image_main_file = self.context['request'].FILES.get('image')
        image_main_url_from_data = validated_data.get('image') # Valor do campo 'image' vindo do request.data

        if image_main_file:
            instance.image_main = image_main_file
        elif image_main_url_from_data and not image_main_url_from_data.startswith('blob:'):
            instance.image_main = image_main_url_from_data
        elif 'image' in validated_data and validated_data['image'] is None: # Se a imagem foi explicitamente setada para None/null
            instance.image_main = None
        # else: Se o campo 'image' não foi enviado (nem como file, nem como url) e não foi null, mantém o valor existente no instance

        instance.save()

        if 'images_meta' in self.context['request'].data: # APENAS se for carrossel e meta de imagens foi enviado
            instance.images.all().delete() 

            images_meta_str = self.context['request'].data.get('images_meta', '[]')
            images_meta = json.loads(images_meta_str) if isinstance(images_meta_str, str) else images_meta_str

            for idx, img_meta in enumerate(images_meta):
                image_file_key = f'images_files[{idx}]'
                image_file = self.context['request'].FILES.get(image_file_key)

                if image_file:
                    GalleryImage.objects.create(
                        post=instance,
                        image=image_file,
                        alt_text=img_meta.get('alt_text', ''),
                        link=img_meta.get('link', ''),
                        order=img_meta.get('order', idx)
                    )
                elif 'image' in img_meta and img_meta['image'] and not img_meta['image'].startswith('blob:'):
                    GalleryImage.objects.create(
                        post=instance,
                        image=img_meta['image'],
                        alt_text=img_meta.get('alt_text', ''),
                        link=img_meta.get('link', ''),
                        order=img_meta.get('order', idx)
                    )
        return instance

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'excerpt', 'content', 'image', 'created_at', 'updated_at']