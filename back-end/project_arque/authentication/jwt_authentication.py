from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed

class FormDataJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header:
            try:
                raw_token = self.get_raw_token(header)
                if raw_token:
                    validated_token = self.get_validated_token(raw_token)
                    return self.get_user(validated_token), validated_token
            except InvalidToken:
                pass
            except AuthenticationFailed:
                pass

        auth_token_from_body = request.data.get('auth_token')
        if auth_token_from_body:
            try:
                validated_token = self.get_validated_token(auth_token_from_body)
                return self.get_user(validated_token), validated_token
            except InvalidToken:
                pass
            except AuthenticationFailed:
                pass

        auth_token_from_query_param = request.query_params.get('token')
        if auth_token_from_query_param:
            try:
                validated_token = self.get_validated_token(auth_token_from_query_param)
                return self.get_user(validated_token), validated_token
            except InvalidToken as e:
                raise AuthenticationFailed(f'Token de autenticação inválido na URL: {e}')
            except AuthenticationFailed as e:
                raise AuthenticationFailed(f'Falha na autenticação via URL: {e}')
        
        return None