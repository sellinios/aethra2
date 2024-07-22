from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Health check view
def health_check(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
    path('healthz/', health_check),  # Add the health check endpoint
]
