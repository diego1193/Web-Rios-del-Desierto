"""
URL configuration for web_sac project.

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
from django.urls import path, include
from clients import views as client_views
from reports import views as report_views
from django.http import HttpResponse

def debug_view(request):
    return HttpResponse("Debug view is working!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', client_views.search_client, name='search_client'),
    path('add-client/', client_views.add_client, name='add_client'),
    path('api/search-client/', client_views.search_client_api, name='search_client_api'),
    path('export-client/<int:client_id>/<str:format_type>/', client_views.export_client_data, name='export_client_data'),
    path('reports/loyalty/', report_views.generate_loyalty_report, name='loyalty_report'),
    path('reports/loyalty/download/', report_views.download_loyalty_report, name='download_loyalty_report'),
    path('debug/', debug_view, name='debug'),
    path('reports/purchases/', report_views.manage_purchases, name='manage_purchases'),
    path('reports/purchases/template/', report_views.download_purchase_template, name='download_purchase_template'),
    path('api/search-clients/', report_views.search_clients_api, name='search_clients_api'),
]
