
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Hotpointentry, name='Hotpointentry'),
    path('Hotpointproduct/', views.Hotpointproduct, name='Hotpointproduct'),
    path('export_users_csv/', views.export_users_csv, name='export_users_csv')
]
