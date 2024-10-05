"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Author Haven API",
        default_version="v1.0",
        description="Author Haven API documentation",
        Contact=openapi.Contact(email="contact@authorhavenapicom"),
        License=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            (
                [
                    path(
                        "schema/",
                        include(
                            [
                                path(
                                    "",
                                    SpectacularAPIView.as_view(),
                                    name="schema-spectacular",
                                ),
                                path(
                                    "swagger/",
                                    SpectacularSwaggerView.as_view(
                                        url_name="schema-spectacular"
                                    ),
                                    name="schema-swagger-ui",
                                ),
                                path(
                                    "redoc/",
                                    SpectacularRedocView.as_view(
                                        url_name="schema-spectacular"
                                    ),
                                    name="schema-redoc",
                                ),
                            ]
                        ),
                    ),
                    path("", include("core_apps.users.urls")),
                ]
            )
        ),
    ),
]

admin.site.site_header = "Authors Haven API Admin"

admin.site.site_title = "Authors Haven API Admin Portal"

admin.site.index_title = "Welcome to Authors Haven API Portal"
