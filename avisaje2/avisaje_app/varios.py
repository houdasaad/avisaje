from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import hashlib
from docx import Document
from reportlab.pdfgen import canvas


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

        # Agregar firma digital
        signed_pdf_path, cve = add_signature(pdf_file_path)

        return render(request, 'success.html', {'signed_pdf_path': signed_pdf_path, 'cve': cve})

    return render(request, 'upload.html')


from docx2pdf import convert

def convert_to_pdf(word_file_path):
    # Ruta del archivo PDF generado
    pdf_file_path = word_file_path.replace('.docx', '.pdf')

    # Convertir el archivo Word a PDF
    convert(word_file_path, pdf_file_path)

    # Retornar la ruta del archivo PDF generado
    return pdf_file_path


def add_signature(pdf_file_path):
    signed_pdf_path = pdf_file_path.replace('.pdf', '_signed.pdf')

    # Cálculo del hash del archivo PDF firmado
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        pdf_hash = hashlib.sha256(pdf_content).hexdigest()

    # Generación del código CVE
    cve = f"CVE-{pdf_hash[:8]}-{pdf_hash[8:16]}-{pdf_hash[16:24]}-{pdf_hash[24:32]}"

    # Aquí iría el código para agregar una firma digital al archivo PDF

    # Retornar la ruta del archivo PDF con la firma digital y el CVE
    return signed_pdf_path, cve




#############

from django.shortcuts import render
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage
import hashlib


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
