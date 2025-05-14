from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import User, Challenge, Task, Achievement, UserChallenge, UserTask, UserStat
from .views import UserTaskViewSet
from rest_framework import status
from django.urls import reverse


class UserTaskTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@test.com', username='test_user', password='test')

        self.test_task_one = Task.objects.create(title='test_task_one')
        self.test_task_two = Task.objects.create(title='test_task_two')
        self.test_achievement = Achievement.objects.create(title='test', points_required=5)
        self.test_challenge = Challenge.objects.create(title='test_challenge', goal='test_goal', achievement=self.test_achievement)
        self.test_challenge.tasks.add(self.test_task_one, self.test_task_two)

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
  
class UserStatTest(TestCase):
    def test_create(self):
        test_user = User.objects.create(email='test@test.com', username='test_user', password='test')

        test_userstat = UserStat.objects.get(pk=1)
        self.assertEqual(test_userstat.user, test_user)

class UserGroupTest(APITestCase):
    def setUp(self):
        

        

