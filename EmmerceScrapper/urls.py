
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotpoint/', include('Hotpoint.urls')),
    path('mika/', include('Mika.urls')),
    path('hypermart/', include('Hypermart.urls')),
    path('opalnet/', include('Opalnet.urls')),
]
