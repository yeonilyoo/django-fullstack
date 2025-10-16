from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r"question", QuestionViewSet)
router.register(r"answer", AnswerViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

"""
POST http://127.0.0.1:8000/api/token/ with body:
{
  "username": "id",
  "password": "password"
}

then something like
GET http://127.0.0.1:8000/api/question/600
with header:
Authorization: Bearer {your_token}
"""
