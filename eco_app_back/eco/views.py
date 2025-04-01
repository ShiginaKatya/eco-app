# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import UserSerializer, RoleSerializer, CategorySerializer, HabitSerializer, FormSerializer, UserPlanSerializer, UserHabitSerializer, AchievementSerializer, UserAchievementSerializer, ChallengeSerializer, TaskSerializer, UserChallengeSerializer, UserTaskSerializer, UserStatSerializer, LevelSerializer
from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, Achievement, UserAchievement, Task, Challenge, UserChallenge, UserTask, UserStat, Level
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

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
        return UserPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
            all_habits_true = all(habit.status for habit in user_plan.habits.all())
            sum_points = 0
            user_plan.status = all_habits_true
            user_plan.save()
            if (user_plan.status == True):
                for habit in user_plan.habits.all():
                    sum_points += habit.habit.difficulty_level
                user_stat = get_object_or_404(UserStat, user = self.request.user)
                user_stat.points += sum_points
                user_stat.save()
                achievement_all = Achievement.objects.all()
                for achievement in achievement_all:
                    if (sum_points == achievement.points_required):
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
        return UserChallenge.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserTaskViewSet(viewsets.ModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class UserStatViewSet(viewsets.ModelViewSet):
    queryset = UserStat.objects.all()
    serializer_class = UserStatSerializer

    def get_queryset(self):
        return UserStat.objects.filter(user=self.request.user)



    