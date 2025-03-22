from rest_framework import routers
from eco.views import UserViewSet, RoleViewSet

router = routers.DefaultRouter()

router.register('roles', RoleViewSet )
router.register('users', UserViewSet) 
