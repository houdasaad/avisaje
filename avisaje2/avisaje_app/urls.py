"""
URL configuration for avisaje_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import upload_file, cotizacion, pago_aviso, listado, iniciar_pago

from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_file/', upload_file, name='upload_file'),
    path('cotizacion/', cotizacion, name='cotizacion'),
    path('pago_aviso/', pago_aviso, name='pago_aviso'),
    path('listado/', listado, name='listado'),
    path('', cotizacion, name='cotizacion'),
    path('buscar/', listado, name='buscar_aviso'),
    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('listado/', views.opciones, name='listado'),
    path('descargar-pdf/<str:nombre_archivo>/', views.descargar_pdf, name='descargar_pdf')
]
