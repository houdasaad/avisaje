# Generated by Django 4.2.2 on 2023-06-15 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisaje_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='archivo_pdf',
            field=models.FileField(blank=True, upload_to='pdfs/'),
        ),
    ]
