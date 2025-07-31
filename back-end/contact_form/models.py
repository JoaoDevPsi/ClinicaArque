from django.db import models

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contato de {self.name} ({self.email})"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contato Recebido"
        verbose_name_plural = "Contatos Recebidos"