# back-end/project_arque/authentication/jwt_authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed

class FormDataJWTAuthentication(JWTAuthentication):
    """
    Classe de autenticação JWT que verifica o token no cabeçalho Authorization,
    no campo 'auth_token' do corpo da requisição (para FormData),
    e como um parâmetro de consulta 'token' na URL.
    """
    def authenticate(self, request):
        # Tenta autenticar via cabeçalho Authorization padrão
        header = self.get_header(request)
        if header:
            try:
                raw_token = self.get_raw_token(header)
                if raw_token:
                    validated_token = self.get_validated_token(raw_token)
                    return self.get_user(validated_token), validated_token
            except InvalidToken:
                pass # Ignorar e tentar outros métodos
            except AuthenticationFailed:
                pass # Ignorar e tentar outros métodos

        # Tenta buscar o token no corpo da requisição (para FormData)
        # (Isso foi uma tentativa anterior, manter para compatibilidade ou remover se desnecessário)
        auth_token_from_body = request.data.get('auth_token')
        if auth_token_from_body:
            try:
                validated_token = self.get_validated_token(auth_token_from_body)
                return self.get_user(validated_token), validated_token
            except InvalidToken:
                pass
            except AuthenticationFailed:
                pass

        # NOVO: Tenta buscar o token no parâmetro de consulta da URL
        auth_token_from_query_param = request.query_params.get('token')
        if auth_token_from_query_param:
            try:
                validated_token = self.get_validated_token(auth_token_from_query_param)
                return self.get_user(validated_token), validated_token
            except InvalidToken as e:
                # Se o token na URL é inválido, levanta exceção para detalhe
                raise AuthenticationFailed(f'Token de autenticação inválido na URL: {e}')
            except AuthenticationFailed as e:
                raise AuthenticationFailed(f'Falha na autenticação via URL: {e}')
        
        # Se não encontrou token em nenhum lugar, retorna None
        return None