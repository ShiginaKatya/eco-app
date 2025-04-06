from rest_framework import routers
from eco.views import UserViewSet, RoleViewSet, CategoryViewSet, HabitViewSet, FormViewSet, UserPlanViewSet, UserHabitViewSet, AchievementViewSet, UserAchievementViewSet, ChallengeViewSet, TaskViewSet, UserChallengeViewSet, UserTaskViewSet, UserStatViewSet, LevelViewSet, FormQuestionViewSet, UserAnswerViewSet, AdviceViewSet, GuideViewSet, FavoriteViewSet, EventViewSet

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
router.register('challenges', ChallengeViewSet) 
router.register('tasks', TaskViewSet)
router.register('userchallenges', UserChallengeViewSet) 
router.register('usertasks', UserTaskViewSet)
router.register('levels', LevelViewSet) 
router.register('userstats', UserStatViewSet)
router.register('questions', FormQuestionViewSet)
router.register('answers', UserAnswerViewSet)
router.register('advices', AdviceViewSet)
router.register('guides', GuideViewSet)
router.register('favorites', FavoriteViewSet)
router.register('events', EventViewSet)

