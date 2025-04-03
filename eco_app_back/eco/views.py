# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import UserSerializer, RoleSerializer, CategorySerializer, HabitSerializer, FormSerializer, UserPlanSerializer, UserHabitSerializer, AchievementSerializer, UserAchievementSerializer, ChallengeSerializer, TaskSerializer, UserChallengeSerializer, UserTaskSerializer, UserStatSerializer, LevelSerializer
from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, Achievement, UserAchievement, Task, Challenge, UserChallenge, UserTask, UserStat, Level
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
import random

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

class UserPlanViewSet(viewsets.ModelViewSet):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer

    def get_queryset(self):
        return UserPlan.objects.filter(user=self.request.user, status=False)

    def perform_create(self, serializer):
        forms = Form.objects.all()
        serializer.save(user=self.request.user, form = random.choice(forms))

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class UserAchievementViewSet(viewsets.ModelViewSet):
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer


class UserHabitViewSet(viewsets.ModelViewSet):
    queryset = UserHabit.objects.all()
    serializer_class = UserHabitSerializer

    def partial_update(self, request, pk=None):
        user_habit = get_object_or_404(UserHabit, pk=pk)
        serializer = UserHabitSerializer(user_habit, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            user_plan = user_habit.plan
            habits_status = all(habit.status for habit in user_plan.habits.all())
            sum_points = 0
            user_plan.status = habits_status
            user_plan.save()
            if user_plan.status == True:
                for habit in user_plan.habits.all():
                    sum_points += habit.habit.difficulty_level
                user_stat = get_object_or_404(UserStat, user = self.request.user)
                user_stat.points += sum_points
                user_stat.save()
                achievement_all = Achievement.objects.all()
                for achievement in achievement_all:
                    if sum_points == achievement.points_required:
                        user_achievement = UserAchievement.objects.create(user = self.request.user, achievement = achievement)
                        achievement_serializer = UserAchievementSerializer(user_achievement, context={'request': request})
                        return Response({'habit': serializer.data,'achievement': achievement_serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserChallengeViewSet(viewsets.ModelViewSet):
    queryset = UserChallenge.objects.all()
    serializer_class = UserChallengeSerializer

    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user, status=False)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            challenges = UserChallenge.objects.filter(user=request.user, status=False)
            for challenge in challenges:
                challenge_serializer = UserChallengeSerializer(challenge, context={'request': request})
                if challenge_serializer.data['challenge'] == request.data['challenge']:
                    return Response({'title': 'Челлендж уже добавлен'}, status=status.HTTP_400_BAD_REQUEST)
                    break
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class UserTaskViewSet(viewsets.ModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer

    def partial_update(self, request, pk=None):
        user_task = get_object_or_404(UserTask, pk=pk)
        serializer = UserTaskSerializer(user_task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            user_challenge = user_task.challenge
            user_challenge_status = all(task.status for task in user_challenge.tasks.all())
            user_challenge.status = user_challenge_status
            user_challenge.save()
            if user_challenge.status == True:
                achievement = user_challenge.challenge.achievement
                user_achievement = UserAchievement.objects.create(user = self.request.user, achievement = achievement)
                user_stat = get_object_or_404(UserStat, user = self.request.user)
                user_stat.points += achievement.points_required
                user_stat.save()
                achievement_serializer = UserAchievementSerializer(user_achievement, context={'request': request})
                return Response({'task': serializer.data,'achievement': achievement_serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class UserStatViewSet(viewsets.ModelViewSet):
    queryset = UserStat.objects.all()
    serializer_class = UserStatSerializer

    def get_queryset(self):
        return UserStat.objects.filter(user=self.request.user)



    