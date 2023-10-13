from django.shortcuts import render, redirect
from PyPDF2 import PdfFileWriter, PdfFileReader
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


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        # Guardar el archivo Word
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # Ruta del archivo Word
        word_file_path = fs.path(filename)

        # Convertir a PDF
        pdf_file_path = convert_to_pdf(word_file_path)

        # Generar el código CVE
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            pdf_hash = hashlib.sha256(pdf_content).hexdigest()
        cve = f"CVE-{pdf_hash[:8]}-{pdf_hash[8:16]}-{pdf_hash[16:24]}-{pdf_hash[24:32]}"

        # Agregar firma digital
        signed_pdf_path = add_signature(pdf_file_path, cve)

        return render(request, 'success.html', {'signed_pdf_path': signed_pdf_path})

    return render(request, 'upload.html')


from docx2pdf import convert

def convert_to_pdf(word_file_path):
    # Ruta del archivo PDF generado
    pdf_file_path = word_file_path.replace('.docx', '.pdf')

    # Convertir el archivo Word a PDF
    convert(word_file_path, pdf_file_path)

    # Retornar la ruta del archivo PDF generado
    return pdf_file_path



def add_signature(pdf_file_path, cve):
    signed_pdf_path = pdf_file_path.replace('.pdf', '_signed.pdf')

    # Cálculo del hash del archivo PDF firmado
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        pdf_hash = hashlib.sha256(pdf_content).hexdigest()

    # Generación del código CVE
    cve = f"CVE-{pdf_hash[:8]}-{pdf_hash[8:16]}-{pdf_hash[16:24]}-{pdf_hash[24:32]}"

    # Código para agregar una firma digital al archivo PDF
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open(pdf_file_path, 'rb'))

    for page_number in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_number)
        page.mergePage(page)
        pdf_writer.addPage(page)

    # Agregar el código CVE al final del PDF
    c = canvas.Canvas(signed_pdf_path)
    c.setFont("Helvetica", 10)
    c.drawString(10, 10, f"Codigo de Verificacion: CVE={cve}")
    c.save()

    # Retornar la ruta del archivo PDF con la firma digital y el CVE
    return signed_pdf_path

def pago_aviso(request):
    return render(request, 'pago_aviso.html')

from django.contrib import messages
from django.urls import reverse

from django.shortcuts import render, redirect
from .models import Cotizacion

from django.shortcuts import render, redirect
from .models import Cotizacion
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


def cotizacion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        text = request.POST.get('text')
        file = request.FILES.get('file')

        if file:  # Si se subió un archivo Word
            text = process(file)  # Obtener el texto del archivo

        # Contar las palabras del texto
        word_count = len(text.split())

        # Calcular el costo
        costo = word_count * 164

        cotizacion = Cotizacion(email=email, texto=text, cantidad_palabras=word_count, costo=costo)
        cotizacion.save()

        # Enviar el email
        subject = 'Cotización de Avisaje Legal'
        message = f'''
            <div style="text-align: center;">
                <p>Estimado cliente,</p>
                <p>El costo de su aviso es de ${costo}.</p>
                <p>¡Muchas gracias!</p>
                <br>
                <a href="{request.build_absolute_uri(reverse('pago_aviso'))}" style="text-decoration: none; background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 4px;">Contratar</a>
            </div>
        '''
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [email], html_message=message)

        messages.success(request, 'Su cotización fue enviada a su email.')

    return render(request, 'cotizacion.html')




from .models import Cotizacion

def listado(request):
    # Obtener todas las cotizaciones de la base de datos ordenadas por fecha descendente
    cotizaciones = Cotizacion.objects.order_by('-fecha')

    return render(request, 'listado.html', {'cotizaciones': cotizaciones})
