
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Mikaentry, name='Mikaentry'),
    path('Mika_reset/', views.Mika_reset, name='Mika_reset'),
    # path('Hotpointproduct/', views.Hotpointproduct, name='Hotpointproduct'),
    path('MikaProducts/', views.MikaProducts, name='MikaProducts'),
    path('export_users_csv/', views.export_users_csv, name='export_users_csv'),
]
