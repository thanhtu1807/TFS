from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, RoleViewSet, GroupViewSet, FunctionViewSet, CriteriaViewSet, AppraisalViewSet, \
    AppraisalFormatViewSet, SessionViewSet, TopicViewSet, CustomObtainAuthToken, logout, reset_token


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'functions', FunctionViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'appraisals', AppraisalViewSet)
router.register(r'appraisal_format', AppraisalFormatViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'criteria', CriteriaViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', CustomObtainAuthToken.as_view()),    
    url(r'^logout/', logout), 
    url(r'^reset_token/', reset_token),
]