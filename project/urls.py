"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import (
    QuestionViewSet,
    AnswerViewSet,
    AnswerListView,
    AnswerDetailView,
    AnswerAcceptView,
    BookmarkListCreateView,
    UserViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register("questions", QuestionViewSet)
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "questions/<int:question_id>/answers",
        AnswerViewSet.as_view({"get": "list", "post": "create"}),
        name="answer-list",
    ),
    path("answers/me", AnswerListView.as_view(), name="my-answers"),
    path("answers/<int:pk>/accept", AnswerAcceptView.as_view(), name="answer-accept"),
    path("answers/<int:pk>", AnswerDetailView.as_view(), name="answer-detail"),
    path("bookmarks/", BookmarkListCreateView.as_view(), name="bookmarks-list"),
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("api-auth/", include("rest_framework.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="drf_spectacular/swagger_ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
