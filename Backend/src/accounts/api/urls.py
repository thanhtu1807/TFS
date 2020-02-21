from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, RoleViewSet, GroupViewSet,CustomObtainAuthToken, logout, reset_token


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', CustomObtainAuthToken.as_view()),    
    url(r'^logout/', logout), 
    url(r'^reset_token/', reset_token),
]