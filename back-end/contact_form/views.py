from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny 


class ContactSubmissionCreateView(generics.CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # CHAVE DA CORREÇÃO: Salvar o objeto e depois acessar seus dados
        contact_submission_instance = serializer.save() # Salva o objeto ContactSubmission

        # Agora, acesse os dados do objeto salvo, incluindo 'submitted_at'
        # que foi adicionado automaticamente ao salvar.
        contact_data = serializer.data # Usa serializer.data para obter a representação completa
                                      # ou o próprio objeto contact_submission_instance
        
        subject = f"Nova Solicitação de Contato: {contact_data['name']}"
        message_body = (
            f"Nome Completo: {contact_data['name']}\n"
            f"Email: {contact_data['email']}\n"
            f"Telefone: {contact_data.get('phone', 'Não informado')}\n"
            f"Mensagem: {contact_data.get('message', 'Nenhuma mensagem adicional')}\n"
            # Acessa submitted_at do objeto salvo
            f"Enviado em: {contact_submission_instance.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}" 
        )
        
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['clinicaarque.psi@gmail.com']

        try:
            send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)
            print(f"E-mail enviado com sucesso para {recipient_list}")
        except Exception as e:
            print(f"ERRO ao enviar e-mail: {e}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)