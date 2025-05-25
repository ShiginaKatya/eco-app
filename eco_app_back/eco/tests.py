from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import User, Challenge, Task, Achievement, UserChallenge, UserTask, UserStat, Habit, UserPlan, UserHabit, UserAchievement, Level, Role, Event, Guide, Advice, Favorite
from .views import UserTaskViewSet, UserHabitViewSet, UserChallengeViewSet, ChallengeViewSet, EventViewSet, UserGroupViewSet, FavoriteViewSet
from rest_framework import status
from django.urls import reverse
from django.utils import timezone


class UserTaskTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')
        self.test_userstat = UserStat.objects.create(user=self.test_user)
        self.test_task_one = Task.objects.create(title='test_task_one')
        self.test_task_two = Task.objects.create(title='test_task_two')
        self.test_achievement = Achievement.objects.create(title='test', points_required=5)
        self.test_challenge = Challenge.objects.create(title='test_challenge', goal='test_goal', achievement=self.test_achievement)
        self.test_challenge.tasks.add(self.test_task_one)

        self.test_userchallenge = UserChallenge.objects.create(challenge = self.test_challenge, user = self.test_user, status=False)
        test_usertask_one = UserTask.objects.create(id = 1, challenge = self.test_userchallenge, task = self.test_task_one, status=False)
        self.factory = APIRequestFactory()
        self.url = reverse('usertask-detail', args=[test_usertask_one.id])

    def test_patch_true(self):
        test_usertask_two = UserTask.objects.create(id = 2, challenge = self.test_userchallenge, task = self.test_task_two, status=True)
        test_request = self.factory.patch(self.url, {'status': True}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserTaskViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        
        test_usertask = UserTask.objects.get(pk=1)
        self.assertTrue(test_usertask.status)

        test_userchallenge = UserChallenge.objects.get(pk=test_usertask.challenge.id)
        self.assertTrue(test_userchallenge.status)

        self.assertIn('achievement', test_response.data)

    def test_patch_false(self):
        test_usertask_two = UserTask.objects.create(id = 2, challenge = self.test_userchallenge, task = self.test_task_two, status=False)
        test_request = self.factory.patch(self.url, {'status': True}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserTaskViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        
        test_usertask = UserTask.objects.get(pk=1)
        self.assertTrue(test_usertask.status)

        test_userchallenge = UserChallenge.objects.get(pk=test_usertask.challenge.id)
        self.assertFalse(test_userchallenge.status)

        self.assertNotIn('achievement', test_response.data)
  
class UserHabitTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')
        self.test_achievement = Achievement.objects.create(title='test', points_required=5)
        self.test_userstat = UserStat.objects.create(user=self.test_user)
        self.test_habit_one = Habit.objects.create(id=1, title='test_habit', difficulty_level=3)
        self.test_habit_two = Habit.objects.create(id=2, title='test_habit', difficulty_level=2)

        self.test_userplan = UserPlan.objects.create(user=self.test_user, goal='test_goal')
        test_userhabit_one = UserHabit.objects.create(id=1, plan=self.test_userplan, habit=self.test_habit_one)

        self.factory = APIRequestFactory()
        self.url = reverse('userhabit-detail', args=[test_userhabit_one.id])

    def test_patch_true(self):
        test_userhabit_two = UserHabit.objects.create(id=2, plan = self.test_userplan, habit = self.test_habit_two, status=True)
        test_request = self.factory.patch(self.url, {'status': True}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserHabitViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        
        test_userhabit = UserHabit.objects.get(pk=1)
        self.assertTrue(test_userhabit.status)

        test_userplan = UserPlan.objects.get(pk=self.test_userplan.id)
        self.assertTrue(test_userplan.status)

        self.assertIn('achievement', test_response.data)
    
    def test_patch_false(self):
        test_userhabit_two = UserHabit.objects.create(id=2, plan = self.test_userplan, habit = self.test_habit_two, status=False)
        test_request = self.factory.patch(self.url, {'status': True}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserHabitViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        
        test_userhabit = UserHabit.objects.get(pk=1)
        self.assertTrue(test_userhabit.status)

        test_userplan = UserPlan.objects.get(pk=self.test_userplan.id)
        self.assertFalse(test_userplan.status)

        self.assertNotIn('achievement', test_response.data)

class UserChallengeTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')
        self.test_achievement = Achievement.objects.create(title='test', points_required=5)
        self.test_challenge = Challenge.objects.create(id=1, title='test_challenge', goal='test_goal', achievement=self.test_achievement)
        self.test_challenge_other = Challenge.objects.create(id=2, title='test_challenge_other', goal='test_goal_other', achievement=self.test_achievement)
        self.test_challenge_url = reverse('challenge-detail', kwargs={'pk': self.test_challenge.pk})
        # self.test_userchallenge_one = UserChallenge.objects.create(challenge = self.test_challenge, user = self.test_user, status=False)
        self.factory = APIRequestFactory()
        self.url = reverse('userchallenge-list')

    def test_post_true(self):
        post_data = {
            'challenge': self.test_challenge_url, 
            'status': False
        }
        test_request = self.factory.post(self.url, post_data, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserChallengeViewSet.as_view({'post': 'create'})
        test_response = test_view(test_request)

        self.assertEqual(test_response.status_code, status.HTTP_201_CREATED)

        # test_userchallenge = UserChallenge.objects.get(pk=2)
        # print(test_userchallenge)
    
    def test_post_false(self):
        UserChallenge.objects.create(challenge = self.test_challenge, user = self.test_user, status=False)
        post_data = {
            'challenge':  self.test_challenge_url, 
            'status': False
        }
        test_request = self.factory.post(self.url, post_data, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserChallengeViewSet.as_view({'post': 'create'})
        test_response = test_view(test_request)

        self.assertEqual(test_response.status_code, status.HTTP_400_BAD_REQUEST)
        
class UserStatTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')
        self.test_level = Level.objects.create(title='test_level', min_points=0)
        self.test_nextlevel = Level.objects.create(title='test_nextlevel', min_points=5)
        self.test_userstat = UserStat.objects.create(user=self.test_user)
        
        self.test_achievement = Achievement.objects.create(title='test', points_required=5)
        self.test_achievement_other = Achievement.objects.create(title='test_other', points_required=5)
        self.test_userachievement = UserAchievement.objects.create(achievement = self.test_achievement, user=self.test_user)
        self.test_userachievement_other = UserAchievement.objects.create(achievement = self.test_achievement_other, user=self.test_user)

        self.test_userplan = UserPlan.objects.create(user=self.test_user, goal='test_goal', status=True)

    def test_achievements_stat(self):
        self.assertEqual(self.test_userstat.achievements_count, UserAchievement.objects.filter(user=self.test_user).count())
        self.assertIn({'achievement': self.test_achievement, 'count': 1 }, self.test_userstat.all_achievements)
        self.assertIn({'achievement': self.test_achievement_other, 'count': 1 }, self.test_userstat.all_achievements)
    
    def test_level_stat(self):
        self.assertEqual(self.test_userstat.level, self.test_level)

    def test_nextlevel_stat(self):
        self.assertEqual(self.test_userstat.next_level, self.test_nextlevel)
    
    def test_completed_plans_stat(self):
        self.assertEqual(self.test_userstat.completed_plans, 1)

class ChallengeTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')
        self.test_achievement = Achievement.objects.create(title='test', points_required=5)
        self.test_challenge = Challenge.objects.create(id=1, title='test_challenge', goal='test_goal', achievement=self.test_achievement)
        
        self.factory = APIRequestFactory()
        self.url = reverse('challenge-detail', args=[self.test_challenge.id])

    def test_patch_week_true(self):
        test_request = self.factory.patch(self.url, {'this_week': True}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = ChallengeViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_challenge = Challenge.objects.get(pk=1)

        self.assertEqual(test_challenge.this_week_date.date(), timezone.now().date())
        self.assertTrue(test_challenge.this_week)
    
    def test_patch_week_false(self):
        test_request = self.factory.patch(self.url, {'this_week': False}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = ChallengeViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_challenge = Challenge.objects.get(pk=1)

        self.assertIsNone(test_challenge.this_week_date)
        self.assertFalse(test_challenge.this_week)

class EventTest(APITestCase):
    def setUp(self):
        self.test_role = Role.objects.create(title='Организация')
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test', role=self.test_role)
        self.test_date = timezone.now().date() + timezone.timedelta(days=5)
        self.test_event = Event.objects.create(title='test_event', event_date=self.test_date, user=self.test_user)
        
        self.factory = APIRequestFactory()
        self.url = reverse('event-detail', args=[self.test_event.id])
    
    def test_patch_date(self):
        test_request = self.factory.patch(self.url, {'event_date': '2025-05-23'}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = EventViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_event = Event.objects.get(pk=1)

        self.assertEqual(test_event.status, 'Перенесено')
    
    def test_patch_same_date(self):
        test_request = self.factory.patch(self.url, {'event_date': '2025-05-26'}, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = EventViewSet.as_view({'patch': 'partial_update'})
        test_response = test_view(test_request, pk=1)

        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_event = Event.objects.get(pk=1)

        self.assertEqual(test_event.status, 'Назначено')
        
class UserGroupTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')
        self.test_member_user = User.objects.create(email='member@test.com', username='member_user', password='test')

        self.factory = APIRequestFactory()
        self.url = reverse('usergroup-list')

    def test_post_group_true(self):
        test_post_data = {
            'title':  'test_title_group', 
            'members': [{
                    'user': reverse('user-detail', kwargs={'pk': self.test_member_user.pk}),
                    'is_confirm': False
                },
                {
                    'user': reverse('user-detail', kwargs={'pk': self.test_user.pk}),
                    'is_confirm': True
                }
            ]
        }
        test_request = self.factory.post(self.url, test_post_data, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserGroupViewSet.as_view({'post': 'create'})
        test_response = test_view(test_request)

        self.assertEqual(test_response.status_code, status.HTTP_201_CREATED)
    
    def test_post_group_false(self):
        test_post_data = {
            'title':  'test_title_group', 
        }
        test_request = self.factory.post(self.url, test_post_data, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = UserGroupViewSet.as_view({'post': 'create'})
        test_response = test_view(test_request)

        self.assertEqual(test_response.status_code, status.HTTP_400_BAD_REQUEST)

class FavoriteTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')
        self.test_guide = Guide.objects.create(title='test_guide')
        self.test_guide_other = Guide.objects.create(title='test_guide_other')
        
        self.factory = APIRequestFactory()
        self.url = reverse('favorite-list')
    
    def test_post_true(self):
        test_post_data = {
            'user' : reverse('user-detail', kwargs={'pk': self.test_user.pk}),
            'guide': reverse('guide-detail', kwargs={'pk': self.test_guide.pk}),
            'favorite_type': 'G',
            'advice': ''
        }
        test_request = self.factory.post(self.url, test_post_data, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = FavoriteViewSet.as_view({'post': 'create'})
        test_response = test_view(test_request)

        self.assertEqual(test_response.status_code, status.HTTP_201_CREATED)
    
    def test_post_false(self):
        Favorite.objects.create(user=self.test_user, guide=self.test_guide, favorite_type='G')
        test_post_data = {
            'user' : reverse('user-detail', kwargs={'pk': self.test_user.pk}),
            'guide': reverse('guide-detail', kwargs={'pk': self.test_guide.pk}),
            'favorite_type': 'G',
            'advice': ''
        }
        test_request = self.factory.post(self.url, test_post_data, format='json')
        force_authenticate(test_request, user=self.test_user)
        test_view = FavoriteViewSet.as_view({'post': 'create'})
        test_response = test_view(test_request)

        self.assertEqual(test_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', test_response.data)

