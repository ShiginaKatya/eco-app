from rest_framework import routers
from eco.views import UserViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet) 