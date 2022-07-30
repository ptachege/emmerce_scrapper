from django.urls import path
from . import views


urlpatterns = [
    path('', views.Hypermart_entry, name='Hypermart_entry'),
    path('Hypermarttproduct/', views.Hypermarttproduct, name='Hypermarttproduct'),
    path('export_users_csv/', views.export_users_csv, name='export_users_csv'),
    # path('hypermart_reset/', views.hypermart_reset, name='hypermart_reset'),
]
