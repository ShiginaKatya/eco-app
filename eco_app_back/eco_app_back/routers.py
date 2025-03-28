from rest_framework import routers
from eco.views import UserViewSet, RoleViewSet, CategoryViewSet, HabitViewSet, FormViewSet, UserPlanViewSet, UserHabitViewSet, AchievementViewSet, UserAchievementViewSet

router = routers.DefaultRouter()

router.register('roles', RoleViewSet )
router.register('users', UserViewSet) 
router.register('categories', CategoryViewSet) 
router.register('habits', HabitViewSet) 
router.register('forms', FormViewSet) 
router.register('userplans', UserPlanViewSet) 
router.register('userhabits', UserHabitViewSet) 
router.register('achievements', AchievementViewSet) 
router.register('userachievements', UserAchievementViewSet)
