from django.urls import path
from . import views

urlpatterns = [
    path('delete_products/', views.delete_products, name='delete_products'),
    path('Hotpointentry/', views.Hotpointentry, name='Hotpointentry'),
    path('Hotpointproduct/', views.Hotpointproduct, name='Hotpointproduct'),
    path('Hypermart_entry/', views.Hypermart_entry, name='Hypermart_entry'),
    path('Hypermarttproduct/', views.Hypermarttproduct, name='Hypermarttproduct'),
    path('Mikaentry/', views.Mikaentry, name='Mikaentry'),
    path('MikaProducts/', views.MikaProducts, name='MikaProducts'),
    path('Opalnet_entry/', views.Opalnet_entry, name='Opalnet_entry'),
    path('Opalnetproduct/', views.Opalnetproduct, name='Opalnetproduct'),
    path('start_scrap/', views.start_scrap, name='start_scrap'),
    path('reset_scrap/', views.reset_scrap, name='reset_scrap'),

    path('samsutech_links/', views.samsutech_links, name='samsutech_links'),
    path('reset_samutech/', views.reset_samutech, name='reset_samutech'),
    path('johnson_links/', views.johnson_links, name='johnson_links'),

]
