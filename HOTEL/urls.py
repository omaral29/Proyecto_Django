"""HOTEL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from HOTEL_APP import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index),
    path('registro/', views.registro),
    path('login/', views.login),
    path('menu/', views.menu_habitaciones),
    path('actualizar_datos/', views.actualizar_datos_usuario ),
    path('reservar/<codigo>/<precio>', views.reservar_habitacion), 
    path('logout/', views.logout),
    path('crudusers', views.crudusersshow),
    path('eliminarusuario/<codigo>', views.eliminarusuario),
    path('actualizarusuario/<codigo>', views.actualizarusuario),
    path('actualizarusuario1/<codigo>', views.actualizarusuario1),
    path('reportes/', views.reportes),
    path('habitacionescrud/', views.habitacionescrud),
    path('actualizarhabitacion/<codigo>', views.actualizarhabitacion),
    path('eliminarhabitacion/<codigo>', views.eliminarhabitacion),
    path('crudtipos', views.crudtipos),
    path('eliminartipo/<codigo>', views.eliminartipo),
    path('actualizartipo/<codigo>', views.actualizartipo),
    path('reporteusuario/', views.reporteusuario),
    path('reportehabitaciones/', views.reportehabitaciones),
    path('reportereserva/', views.reportereserva),
    path('reportepagos/', views.reportepagos),
    path('reportetomadedecisiones/', views.reportetomadedecisiones),
    path('misreportes/', views.misreportes),
    path('pago/', views.process_payment),
    path('misreservas/', views.misreportes),
    path('ads1/', views.ads1),
    path('ads2/', views.ads2),
    path('ads3/', views.ads3),
    path('pdf1/', views.my_view),
    path('pdf2/', views.my_view2),
    path('pdf3/', views.my_view3),



]
