
from django.shortcuts import render, redirect
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage
import hashlib


import PyPDF2


def add_signature(pdf_file_path):
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

add_signature('test.pdf')