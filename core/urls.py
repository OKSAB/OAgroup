from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('services/legal/', views.service_legal_view, name='service_legal'),
    path('services/corporate/', views.service_corporate_view, name='service_corporate'),
    path('contact/', views.contact_view, name='contact'),
    # Preview error pages during development
    path('404/', views.custom_404_view, name='404_preview'),
    path('500/', views.custom_500_view, name='500_preview'),
]
