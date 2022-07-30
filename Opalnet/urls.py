from django.urls import path
from . import views


urlpatterns = [
    path('', views.Opalnet_entry, name='Opalnet_entry'),
    path('Opalnetproduct/', views.Opalnetproduct, name='Opalnetproduct'),
    path('export_users_csv/', views.export_users_csv, name='export_users_csv'),
]
