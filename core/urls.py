from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/accounts/', include("accounts.urls")),
    path('api/auth/', include("authentication.urls")),
    path('api/notifications/', include("notifications.urls")),
    path('api/orders/', include("orders.urls")),
    path('api/products/', include("products.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
