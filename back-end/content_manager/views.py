import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Article, GalleryPost, GalleryImage
from .serializers import ArticleSerializer, GalleryPostSerializer, GalleryImageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class GalleryPostViewSet(viewsets.ModelViewSet):
    queryset = GalleryPost.objects.all()
    serializer_class = GalleryPostSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        print("\n--- DEBUG: Requisição POST para GalleryPost ---")
        print(f"Método HTTP: {request.method}")
        print(f"Headers da requisição: {request.headers}")
        print(f"Corpo da requisição (request.data): {request.data}")
        print(f"Arquivos na requisição (request.FILES): {request.FILES}")
        print(f"Token 'auth_token' no request.data: {request.data.get('auth_token')}")
        print(f"Cabeçalho Authorization: {request.headers.get('Authorization')}")
        print("--- FIM DEBUG ---\n")

        images_meta = []

        image_main_file = request.FILES.get('image_main')
        image_main_url_from_data = request.data.get('image_main')

        gallery_post = GalleryPost.objects.create(
            id=request.data.get('id', None),
            post_type=request.data['post_type'],
            link=request.data.get('link'),
            image_main=image_main_file if image_main_file else (image_main_url_from_data if image_main_url_from_data and not image_main_url_from_data.startswith('blob:') else None)
        )

        if gallery_post.post_type == 'carousel':
            images_meta_str = request.data.get('images_meta', '[]')
            images_meta = json.loads(images_meta_str) if isinstance(images_meta_str, str) else images_meta_str
            for idx, img_meta in enumerate(images_meta):
                image_file_key = f'images_files[{idx}]'
                image_file = request.FILES.get(image_file_key)

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

        serializer = self.get_serializer(instance=gallery_post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        print("\n--- DEBUG: Requisição PUT para GalleryPost ---")
        print(f"Request data PUT:", request.data)
        print(f"Request files PUT:", request.FILES)
        print(f"Auth token from data PUT:", request.data.get('auth_token'))
        print(f"Cabeçalho Authorization PUT:", request.headers.get('Authorization'))
        print("--- FIM DEBUG PUT ---\n")

        return super().update(request, *args, **kwargs)