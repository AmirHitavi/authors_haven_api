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
                                    "swagger<format>/",
                                    schema_view.without_ui(cache_timeout=0),
                                    name="schema-json",
                                ),
                                path(
                                    "swagger/",
                                    schema_view.with_ui("swagger", cache_timeout=0),
                                    name="schema-swagger-ui",
                                ),
                                path(
                                    "redoc/",
                                    schema_view.with_ui("redoc", cache_timeout=0),
                                    name="schema-redoc",
                                ),
                            ]
                        ),
                    ),
                    path("", include("core_apps.users.urls")),
                    path("profiles/", include("core_apps.profiles.urls")),
                    path("articles/", include("core_apps.articles.urls")),
                ]
            )
        ),
    ),
]

admin.site.site_header = "Authors Haven API Admin"

admin.site.site_title = "Authors Haven API Admin Portal"

admin.site.index_title = "Welcome to Authors Haven API Portal"
