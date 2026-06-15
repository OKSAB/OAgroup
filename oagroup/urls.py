from django.contrib import admin
from django.urls import path, include

handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
