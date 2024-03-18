from django.db import models
from django.conf import settings
from django.urls import reverse


class Cotizacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    nombre_archivo = models.TextField(blank=True, null=True)
    texto = models.TextField(blank=True, null=True)
    cantidad_palabras = models.IntegerField(blank=True, null=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    email = models.EmailField()
    archivo_pdf = models.FileField(upload_to="pdfs/", blank=True, null=True)

    def __str__(self):
        return f"Cotizacion {self.id}"

    def get_pdf_url(self):
        if self.archivo_pdf:
            return self.archivo_pdf.url
        return ""

    def get_absolute_url(self):
        return reverse("ver_cotizacion", args=[str(self.id)])
    

class Aviso(models.Model):
    fecha_aviso = models.DateTimeField(auto_now_add=True)
    nombre_archivo = models.TextField(blank=True, null=True)
    text_aviso = models.TextField()
    email = models.EmailField()
    archivo_pdf = models.FileField(upload_to="pdfs/", blank=True, null=True)
    CATEGORIA_CHOICES = [
        ("Balances_y_Estados_Financieros", "Balances y Estados Financieros"),
        ("Citaciones", "Citaciones"),
        (
            "Concesiones_Ministerio_Obras_Públicas",
            "Concesiones Ministerio Obras Públicas",
        ),
        (
            "Concursos,_Sorteos_Letras_Hipotecarias,_Pago_Dividendos,_Emisión_de_Bonos_Bancarios",
            "Concursos, Sorteos Letras Hipotecarias, Pago Dividendos, Emisión de Bonos Bancarios",
        ),
        ("Extractos/Concesiones", "Extractos/Concesiones"),
        (
            "Extraví­o_de_Documentos_y_Ordenes_de_No_Pago",
            "Extraví­o de Documentos y Ordenes de No Pago",
        ),
        ("Extravío_de_Títulos", "Extravío de Títulos"),
        ("Fé_de_erratas", "Fé de erratas"),
        (
            "Hecho_Esencial,_Opción_Preferente,_Disminución_de_Capital,_OPA.",
            "Hecho Esencial, Opción Preferente, Disminución de Capital, OPA.",
        ),
        (
            "Licitaciones,_Ventas,_Remates_y_Propuestas",
            "Licitaciones, Ventas, Remates y Propuestas",
        ),
        ("Ministerio_de_economía", "Ministerio de economía"),
        (
            "Municipalidades,_Extractos_Licitaciones,_Ordenanzas",
            "Municipalidades, Extractos Licitaciones, Ordenanzas",
        ),
        ("Órdenes_de_No_Pago_Banco_BBVA", "Órdenes de No Pago Banco BBVA"),
        ("Órdenes_de_No_Pago_Banco_BCI", "Órdenes de No Pago Banco BCI"),
        ("Órdenes_de_No_Pago_Banco_Bice", "Órdenes de No Pago Banco Bice"),
        (
            "Órdenes_de_No_Pago_Banco_Del_Desarrollo",
            "Órdenes de No Pago Banco Del Desarrollo",
        ),
        ("Órdenes_de_No_Pago_Banco_Estado", "Órdenes de No Pago Banco Estado"),
        ("Órdenes_de_No_Pago_Banco_Falabella", "Órdenes de No Pago Banco Falabella"),
        ("Órdenes_de_No_Pago_Banco_Santander", "Órdenes de No Pago Banco Santander"),
        ("Órdenes_de_No_Pago_Banco_Scotiabank", "Órdenes de No Pago Banco Scotiabank"),
        ("Órdenes_de_No_Pago_ECR_Group", "Órdenes de No Pago ECR Group"),
        ("Órdenes_de_No_Pago_EQUIFAX", "Órdenes de No Pago EQUIFAX"),
        (
            "Órdenes_de_No_pago_Multiservicios_OK",
            "Órdenes de No pago Multiservicios OK",
        ),
        ("OTIC_-_Camara_de_la_Construcción", "OTIC - Camara de la Construcción"),
        ("Otros", "Otros"),
        ("Posesiones_Efectivas", "Posesiones Efectivas"),
        (
            "Posesiones_Efectivas_Registro_Civil_R._Metropolitana",
            "Posesiones Efectivas Registro Civil R. Metropolitana",
        ),
        (
            "Publicaciones_Accionistas_Fallecidos_y_Listado_de_Asegurados_Fallecidos",
            "Publicaciones Accionistas Fallecidos y Listado de Asegurados Fallecidos",
        ),
        ("Publicaciones_FOSIS", "Publicaciones FOSIS"),
        ("Publicaciones_Judiciales", "Publicaciones Judiciales"),
        ("Publicaciones_SERNAC", "Publicaciones SERNAC"),
        ("Publicaciones_Tributarias", "Publicaciones Tributarias"),
        ("Tarifas", "Tarifas"),
    ]

    categoria = models.CharField(
        max_length=255,
        choices=CATEGORIA_CHOICES,
        # default=CATEGORIA_CHOICES[0][0]  # Esto establece un valor por defecto si lo deseas
    )
