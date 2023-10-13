from django.db import models
from django.conf import settings
from django.urls import reverse

class Cotizacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    cantidad_palabras = models.IntegerField()
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    email = models.EmailField()
    archivo_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def __str__(self):
        return f'Cotizacion {self.id}'

    def get_pdf_url(self):
        if self.archivo_pdf:
            return self.archivo_pdf.url
        return ''

    def get_absolute_url(self):
        return reverse('ver_cotizacion', args=[str(self.id)])
