from django.urls import path
from knox import views as knox_views
from rest_framework import routers

from taskban_backend.users.api.views import RegisterAPI, LoginAPI, UserViewSet, UserSearchView

app_name = "users"

router = routers.DefaultRouter()
router.register("", UserViewSet)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('search/', UserSearchView.as_view(), name='user'),
] + router.urls
