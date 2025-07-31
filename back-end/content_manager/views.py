# back-end/content_manager/views.py
import json # Certifique-se de que 'json' está importado no topo
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

    # AQUI ESTÃO AS LINHAS DE DEBUG
    def create(self, request, *args, **kwargs):
        print("\n--- DEBUG: Requisição POST para GalleryPost ---")
        print(f"Método HTTP: {request.method}")
        print(f"Headers da requisição: {request.headers}")
        print(f"Corpo da requisição (request.data): {request.data}")
        print(f"Arquivos na requisição (request.FILES): {request.FILES}")
        print(f"Token 'auth_token' no request.data: {request.data.get('auth_token')}")
        print(f"Cabeçalho Authorization: {request.headers.get('Authorization')}")
        print("--- FIM DEBUG ---\n")

        # Continuar com a lógica de criação (chamar o ModelViewSet.create original)
        # Você tinha customizado o create, então vamos manter a lógica atual.
        # Se você usar o padrão do ModelViewSet, basta remover esta função e as prints.
        # Mas para o teste, precisamos que ela execute.

        # Lógica personalizada para criar GalleryPost com GalleryImage aninhadas
        images_meta = [] 

        # Lógica para image_main para tipo 'single'
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

        serializer = self.get_serializer(instance=gallery_post) # Serializa a instância criada
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # O método 'update' também deve ser ajustado para incluir os prints de debug se quiser depurá-lo
    # (Mas vamos focar no create por enquanto)
    def update(self, request, *args, **kwargs):
        # Adicione prints de debug aqui também se for testar o PUT
        print("\n--- DEBUG: Requisição PUT para GalleryPost ---")
        print(f"Request data PUT:", request.data)
        print(f"Request files PUT:", request.FILES)
        print(f"Auth token from data PUT:", request.data.get('auth_token'))
        print(f"Cabeçalho Authorization PUT:", request.headers.get('Authorization'))
        print("--- FIM DEBUG PUT ---\n")

        # Chama o método update original do superclass ModelViewSet
        return super().update(request, *args, **kwargs) # Ou o seu método update customizado