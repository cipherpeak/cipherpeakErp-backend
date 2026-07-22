"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/organization/', include('apps.organization.urls')),
    path('api/hr/', include('apps.hr.urls')),
    path('api/system/', include('apps.system.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/procurement/', include('apps.procurement.urls')),
    path('api/manufacturing/', include('apps.manufacturing.urls')),
    path('api/quality/', include('apps.quality.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/crm/', include('apps.crm.urls')),
    path('api/sales/', include('apps.sales.urls')),
    path('api/talent/', include('apps.talent.urls')),
    path('api/payroll/', include('apps.payroll.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/tax/', include('apps.tax.urls')),
    path('api/calendar/', include('apps.calendar_app.urls')),
    path('api/ai/', include('apps.ai.urls')),
    path('api/home/', include('apps.home.urls')),
    # --- SWAGGER URLs ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)