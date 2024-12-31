from django.contrib import admin
from django.urls import path,include
from api.views import get_items

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/items/', get_items),
    path('api/', include('api.urls')),
]
