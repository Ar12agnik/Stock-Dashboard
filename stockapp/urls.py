"""
URL configuration for stockapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from stockalert.views import index,logout_user,add_stock,add_sell_record,detailes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='index'),
    path('logout', logout_user,name= 'logout'),
    path('add_stock', add_stock,name= 'add_stock'),
    path('remove_stock', add_sell_record,name= 'remove_stock'),
    path('detailes/<int:pk>',detailes ,name= 'detales tab'),
    
]
