# from django.shortcuts import render

from rest_framework import viewsets
from .serializers import UserSerializer, RoleSerializer, CategorySerializer, HabitSerializer, FormSerializer, UserPlanSerializer, UserHabitSerializer, AchievementSerializer, UserAchievementSerializer, ChallengeSerializer, TaskSerializer, UserChallengeSerializer, UserTaskSerializer, UserStatSerializer, LevelSerializer, FormQuestionSerializer, UserAnswerSerializer, AdviceSerializer, GuideSerializer, FavoriteSerializer, EventSerializer
from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, Achievement, UserAchievement, Task, Challenge, UserChallenge, UserTask, UserStat, Level, FormQuestion, UserAnswer, Advice, Guide, Favorite, Event
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

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

class FormQuestionViewSet(viewsets.ModelViewSet):
    queryset = FormQuestion.objects.all()
    serializer_class = FormQuestionSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserPlanViewSet(viewsets.ModelViewSet):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer

    def get_queryset(self):
        return UserPlan.objects.filter(user=self.request.user, is_done=False)

    def perform_create(self, serializer):
        forms = Form.objects.all()
        serializer.save(user=self.request.user, form = random.choice(forms))
    
    @action(detail=False)
    def latest(self, request):
        plans = UserPlan.objects.filter(user=self.request.user).order_by("-id")[0:1]
        serializer = UserPlanSerializer(plans, many=True, context={'request': request})
        return Response(serializer.data)

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
    
    @action(detail=False)
    def latest(self, request):
        challenges = UserChallenge.objects.filter(user=self.request.user, status=False).order_by("-id")[0:2]
        serializer = UserChallengeSerializer(challenges, many=True, context={'request': request})
        return Response(serializer.data)

    

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

class AdviceViewSet(viewsets.ModelViewSet):
    queryset = Advice.objects.all()
    serializer_class = AdviceSerializer

    @action(detail=False)
    def personal(self, request):
        user_plans = UserPlan.objects.filter(user=self.request.user)
        habits_category = []
        for plan in user_plans:
            habits = UserHabit.objects.filter(plan=plan)
            for habit in habits:
                habit_category = habit.habit.category.title
                habits_category.append(habit_category)
        user_challenges = UserChallenge.objects.filter(user = self.request.user)
        challenges_category = []
        for challenge in user_challenges:
            challenge_category = challenge.challenge.category.title
            challenges_category.append(challenge_category)
        user_categories = habits_category + challenges_category
        categories = Category.objects.all()
        use_categories = {}
        for category in categories:
            use_categories[category] = user_categories.count(category.title)
        use_categories = sorted(use_categories.items(), key=lambda item: item[1])[:2]
        personal_advices = Advice.objects.filter(Q(category = use_categories[0][0]) | Q(category = use_categories[1][0]))
        random_advices = personal_advices.order_by('?')[:3]
        personal_serializer = AdviceSerializer(random_advices, many=True, context={'request': request})
        print(random_advices)
        return Response(personal_serializer.data)

    

        

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['favorite_type']

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            favorites = Favorite.objects.filter(user=request.user)
            for favorite in favorites:
                favorite_serializer = FavoriteSerializer(favorite, context={'request': request})
                if favorite_serializer.data['advice'] == request.data['advice']:
                    return Response({'title': 'Совет уже добавлен'}, status=status.HTTP_400_BAD_REQUEST)
                    break
                if favorite_serializer.data['guide'] == request.data['guide']:
                    return Response({'title': 'Руководство уже добавлено'}, status=status.HTTP_400_BAD_REQUEST)
                    break
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False)
    def latest(self, request):
        favorites = Favorite.objects.filter(user=self.request.user).order_by("-id")[0:5]
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)
    
    # @action(detail=False)
    # def advices(self, request):
    #     advices = Favorite.objects.filter(favorite_type='A')
    #     serializer = FavoriteSerializer(advices, many=True, context={'request': request})
    #     return Response(serializer.data)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

@authentication_classes([JWTAuthentication])
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Success'})

    