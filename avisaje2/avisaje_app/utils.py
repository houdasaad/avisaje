from django.conf import settings
from docx2pdf import convert
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
import os
import tempfile

def convert_word_to_pdf(file):
    # Generar un nombre único para el archivo PDF
    pdf_name = file.name.replace('.docx', '.pdf')

    # Guardar el archivo temporalmente
    with open(f'media/tmp.docx', 'wb') as tmp_file:
        for chunk in file.chunks():
            tmp_file.write(chunk)

    # Convertir el archivo Word a PDF
    convert('media/tmp.docx', f'media/{pdf_name}')

    # Eliminar el archivo temporal
    os.remove('media/tmp.docx')

    # Devolver la ubicación del archivo PDF convertido
    return pdf_name



def convert_text_to_pdf(text, name):
    # Crear el archivo PDF
    pdf_path = os.path.join(settings.MEDIA_ROOT, name)
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Configurar el formato del texto en el PDF
    c.setFont("Helvetica", 12)

    # Escribir el texto en el PDF
    c.drawString(100, 700, text)

    # Finalizar el archivo PDF
    c.save()

    # Leer el contenido del archivo PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    # Eliminar el archivo temporal




def convert_pdf_to_image(pdf_path):
    # Convertir el PDF a imágenes
    images = convert_from_path(pdf_path)

    # Guardar las imágenes (opcional, si necesitas trabajar con ellas)
    for i, image in enumerate(images):
        image_path = os.path.join(settings.MEDIA_ROOT, f'imagen_{i}.png')
        image.save(image_path, 'PNG')
    
    return len(images)


def delete_images(images):
    for i in range(len(images)):
        image_path = os.path.join(settings.MEDIA_ROOT, f'imagen_{i}.png')
        os.remove(image_path)
