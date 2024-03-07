from django.shortcuts import render, redirect
from PyPDF2 import PdfFileWriter, PdfReader
from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage
import hashlib
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from docx2txt import process
from django.urls import reverse
import os
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
import random
from .utils import (
    convert_pdf_to_image,
    convert_word_to_pdf,
    convert_text_to_pdf,
)  # Asegúrate de tener estas funciones en utils.py

import pytz
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.urls import reverse

from django.shortcuts import render, redirect
from .models import Cotizacion

from django.shortcuts import render, redirect
from .models import Cotizacion, Aviso
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from .models import Cotizacion
from .utils import convert_word_to_pdf, convert_text_to_pdf

from django.contrib import messages
from django.urls import reverse
from .models import Cotizacion


import PyPDF2


def upload_file(request):
    if request.method == "POST" and request.FILES["file"]:
        file = request.FILES["file"]

        # Guardar el archivo Word
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # Ruta del archivo Word
        word_file_path = fs.path(filename)

        # Convertir a PDF
        pdf_file_path = convert_to_pdf(word_file_path)

        # Generar el código CVE
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()
            pdf_hash = hashlib.sha256(pdf_content).hexdigest()
        cve = f"CVE-{pdf_hash[:8]}-{pdf_hash[8:16]}-{pdf_hash[16:24]}-{pdf_hash[24:32]}"

        # Agregar firma digital
        signed_pdf_path = add_signature(pdf_file_path, cve)

        return render(request, "success.html", {"signed_pdf_path": signed_pdf_path})

    return render(request, "upload.html")


from docx2pdf import convert


def convert_to_pdf(word_file_path):
    # Ruta del archivo PDF generado
    pdf_file_path = word_file_path.replace(".docx", ".pdf")

    # Convertir el archivo Word a PDF
    convert(word_file_path, pdf_file_path)

    # Retornar la ruta del archivo PDF generado
    return pdf_file_path


def add_signature(pdf_file_path, cve):
    signed_pdf_path = pdf_file_path.replace(".pdf", "_signed.pdf")

    # Cálculo del hash del archivo PDF firmado
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()
        pdf_hash = hashlib.sha256(pdf_content).hexdigest()

    # Generación del código CVE
    cve = f"CVE-{pdf_hash[:8]}-{pdf_hash[8:16]}-{pdf_hash[16:24]}-{pdf_hash[24:32]}"

    # Código para agregar una firma digital al archivo PDF
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfReader(open(pdf_file_path, "rb"))

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        page.mergePage(page)
        pdf_writer.addPage(page)

    # Agregar el código CVE al final del PDF
    c = canvas.Canvas(signed_pdf_path)
    c.setFont("Helvetica", 10)
    c.drawString(10, 10, f"Código de Verificación: CVE={cve}")
    c.save()

    # Retornar la ruta del archivo PDF con la firma digital y el CVE
    return signed_pdf_path


def pago_aviso(request):
    return render(request, "pago_aviso.html")



def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()
        return text
    except Exception as e:
        # Maneja las excepciones que puedan ocurrir al procesar el PDF
        return str(e)


def cotizacion(request):
    if request.method == "POST":
        email = request.POST.get("email")
        text = request.POST.get("text")
        file = request.FILES.get("file")

        if file:  # Verifica si hay un archivo
            storage = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = storage.save(file.name, file)

            if file.name.endswith(".pdf"):
                pdf_filename = file.name
                text = extract_text_from_pdf(file)

            elif file.name.endswith(".doc") or file.name.endswith(".docx"):
                text = process(file)  # Procesar otros tipos de archivo (como Word)
                pdf_filename = convert_word_to_pdf(file)

                # Si el request es texto, convertir a PDF
        elif text:
            pdf_filename = f"Aviso_{random.randint(1, 34564)}.pdf"
            convert_text_to_pdf(text, pdf_filename)

        # Resto de tu lógica aquí

        # Contar las palabras del texto
        word_count = len(text.split())

        # Calcular el costo
        costo = word_count * 80
        request.session["costo"] = costo

        cotizacion = Cotizacion(
            email=email,
            texto=text,
            cantidad_palabras=word_count,
            costo=costo,
            nombre_archivo=pdf_filename,
        )
        cotizacion.save()

        request.session["cotizacion_id"] = cotizacion.id

        # Enviar el email
        subject = "Cotización de Avisaje Legal"
        message = f"""
            <div style="text-align: center;">
                <p>Estimado cliente,</p>
                <p>El costo de su aviso es de <strong>${costo}</strong>.</p>
                <p>Para iniciar el proceso de pago, por favor haga clic en el botón "Iniciar Pago" y será redirigido a nuestra página segura de pago.</p>
                <p>¡Estamos a su disposición para cualquier consulta!</p>
                <br>
                <a href="{request.build_absolute_uri(reverse('iniciar_pago'))}?costo={costo}" style="text-decoration: none; background-color: #4CAF50; color: white; padding: 15px 25px; border-radius: 5px; font-size: 18px; font-weight: bold;">Iniciar Pago</a>
                <br><br>
                <p>Atentamente,</p>
                <p><em>El Equipo de [Nombre de la Empresa]</em></p>
            </div>
        """

        send_mail(
            subject, "", settings.DEFAULT_FROM_EMAIL, [email], html_message=message
        )

        messages.success(request, "Su cotización fue enviada a su email.")

    return render(request, "cotizacion.html")


from .models import Cotizacion


from django.shortcuts import render
from .models import Aviso
from django.db.models import Q
from datetime import datetime


# def listado(request):
#     # Comenzar con todas las cotizaciones
#     cotizaciones_list = Cotizacion.objects.order_by("-fecha")

#     # Búsqueda por palabras en el texto de cotización
#     text_query = request.GET.get("q")
#     if text_query:
#         cotizaciones_list = cotizaciones_list.filter(texto__icontains=text_query)

#     # Búsqueda por rango de fechas
#     start_date = request.GET.get("start_date")
#     end_date = request.GET.get("end_date")
#     if start_date and end_date:
#         start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
#         end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
#         cotizaciones_list = cotizaciones_list.filter(
#             fecha__range=(start_date, end_date)
#         )

#     # Búsqueda por categoría
#     category_query = request.GET.get("category")
#     if category_query:
#         cotizaciones_list = cotizaciones_list.filter(categoria=category_query)

#     # Puedes añadir aquí más filtros si es necesario

#     # Renderizar el mismo template con las cotizaciones filtradas o todas
#     return render(request, "listado.html", {"cotizaciones": cotizaciones_list})

def listado(request):
    # Comenzar con todos los avisos
    avisos_list = Aviso.objects.order_by("-fecha_aviso")
    
    # Búsqueda por palabras en el texto del aviso
    text_query = request.GET.get("q")
    if text_query:
        avisos_list = avisos_list.filter(text_aviso__icontains=text_query)

    # Búsqueda por rango de fechas
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        avisos_list = avisos_list.filter(
            fecha_aviso__range=(start_date, end_date)
        )

    # Búsqueda por categoría
    category_query = request.GET.get("category")
    if category_query:
        avisos_list = avisos_list.filter(categoria=category_query)

    # Puedes añadir aquí más filtros si es necesario

    # Renderizar el mismo template con los avisos filtrados o todos
    return render(request, "listado.html", {"avisos_list": avisos_list})


from django.shortcuts import redirect
import requests

"""
Request simple a la API,
que redirecciona a la pagina de pago.
"""


def iniciar_pago(request):
    costo = request.session.get("costo", 0)
    cotizacion_id = request.session.get("cotizacion_id", 0)

    # Variables globales
    API_URL = r"https://api-prod01.etpayment.com"
    PTM_URL = r"https://pmt-01.etpayment.com"
    INIT_API = r"/session/initialize"
    MERCHANT_CODE = "cl_desenfoque"
    MERCHANT_API_TOKEN = (
        "IITurcPfTCqRUamXzBOhNikvC1YgVp6FetxDpAgPIzyBmYBojRQHr073cAX1iPhX"
    )

    request_data = {
        "merchant_code": MERCHANT_CODE,
        "merchant_api_token": MERCHANT_API_TOKEN,
        "merchant_order_id": "order-1992",  # id de orden de compra propio del comercio
        "order_amount": costo,
        "metadata": [
            {
                "cotizacion_id": cotizacion_id,  # id de la cotización a pagar
                "show": True
            }
        ]
    }

    # Obtención de session token

    resp = requests.post(API_URL + INIT_API, json=request_data)
    if resp.status_code == 200:
        token = resp.json()["token"]
        signature_token = resp.json()["signature_token"]
        payment_url = PTM_URL + "/session/" + token
        # En lugar de usar webbrowser, redirigimos al cliente con Django
        return redirect(payment_url)
    else:
        # Manejar errores aquí
        pass

    # Se lanza sesión del cliente
    # webbrowser.open(PTM_URL+'/session/'+token)


from django.shortcuts import render
from .models import Aviso


def opciones(request):
    categoria_choices = Aviso.CATEGORIA_CHOICES

    # Aquí puedes añadir más lógica según necesites

    return render(request, "listado.html", {"categoria_choices": categoria_choices})


from django.shortcuts import render


def verificar_documento(request):
    if request.method == "POST":
        cve = request.POST.get("cve")

        # Realiza la verificación del código CVE aquí
        # Puedes buscar en tu base de datos si tienes un registro con el mismo CVE

        # Si el CVE es válido, muestra un mensaje de éxito
        if cve_valido:
            mensaje = "El documento es auténtico."
        else:
            mensaje = "El documento no es auténtico o el código CVE es incorrecto."

        return render(request, "verificacion.html", {"mensaje": mensaje})

    return render(request, "verificacion.html", {})


from django.http import HttpResponse


from django.http import FileResponse
import os

from django.http import FileResponse, HttpResponse
from django.conf import settings
import os


def descargar_pdf(request, nombre_archivo):
    # Verifica que el nombre_archivo no esté vacío
    if nombre_archivo:
        # Construye la ruta completa al archivo PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, nombre_archivo)

        # Abre el archivo y devuelve una respuesta de archivo
        try:
            pdf_file = open(pdf_path, "rb")
            response = FileResponse(pdf_file)
            response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
            return response
        except FileNotFoundError:
            return HttpResponse("Archivo no encontrado", status=404)
    else:
        # Maneja el caso en el que el nombre_archivo está vacío
        return HttpResponse("El nombre del archivo no es válido", status=400)


from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import locale


def descargar_certificado(request, aviso_id):
    if aviso_id:
        aviso = Aviso.objects.get(id=aviso_id)
        pdf_path = os.path.join(settings.MEDIA_ROOT, aviso.nombre_archivo)
        nuevo_pdf_path = os.path.join(settings.MEDIA_ROOT, "nuevo_certificado.pdf")
        

        # para que el mes salga en español
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.datetime.now()
        # para eliminar el cero a la izquierda (ej: 05 de marzo de 2024)
        dia = str(fecha_actual.day)
        fecha_actual_formateada = f"{dia} de {fecha_actual.strftime('%B')} de {fecha_actual.year}"

        fecha_aviso = aviso.fecha_aviso
        dia = str(fecha_aviso.day)
        fecha_aviso_formateada = f"{dia} de {fecha_aviso.strftime('%B')} de {fecha_aviso.year}"
        ancho_imagen = A4[0]-72*2  # Mantener relación de aspecto
        alto_imagen = ancho_imagen * 4/3

        # Convertir el PDF a imágenes
        imagenes_count = convert_pdf_to_image(pdf_path)
        # imagenes = convert_from_path(pdf_path)

        # Crear un nuevo PDF
        doc = SimpleDocTemplate(nuevo_pdf_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Encabezado
        story.append(Paragraph("CERTIFICADO DE PUBLICACIÓN LEGAL", styles['Heading2']))

        # Insertar imágenes como párrafos
        for i in range(imagenes_count):
            image_path = os.path.join(settings.MEDIA_ROOT, f'imagen_{i}.png')
            story.append(Image(image_path, width=ancho_imagen, height=alto_imagen))
            # story.append(Spacer(1, 2))

        # Texto de conclusión
        texto_conclusion = f"El contenido de este texto ha estado publicado en la página de aviso legales de DESENFOQUE.CL durante los días {fecha_aviso_formateada} al {fecha_actual_formateada} y estará disponible en el repositorio digital de la Biblioteca Nacional de acuerdo a lo que establece la ley."
        story.append(Paragraph(texto_conclusion, styles['Normal']))
        story.append(Spacer(1, 7))

        logo_path = os.path.join(settings.STATICFILES_DIRS[0],'avisaje_app', 'images', 'logo_desenfoque.png')
        ancho_logo = 300
        alto_logo = ancho_logo * 0.13
        story.append(Image(logo_path, width=ancho_logo, height=alto_logo))

        # Construir el PDF
        doc.build(story)
        try:
            pdf_file = open(nuevo_pdf_path, "rb")
            response = FileResponse(pdf_file)
            nombre, _ = aviso.nombre_archivo.split('.')
            response["Content-Disposition"] = f'attachment; filename="{nombre}_certificado.pdf"'
            return response
        except FileNotFoundError:
            return HttpResponse("Archivo no encontrado", status=404)
    else:
        # Maneja el caso en el que el nombre_archivo está vacío
        return HttpResponse("El id del archivo no es válido", status=400)