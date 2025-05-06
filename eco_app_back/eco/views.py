# from django.shortcuts import render

from rest_framework import viewsets
from .serializers import UserSerializer, RoleSerializer, CategorySerializer, HabitSerializer, FormSerializer, UserPlanSerializer, UserHabitSerializer, AchievementSerializer, UserAchievementSerializer, ChallengeSerializer, TaskSerializer, UserChallengeSerializer, UserTaskSerializer, UserStatSerializer, LevelSerializer, FormQuestionSerializer, UserAnswerSerializer, AdviceSerializer, GuideSerializer, FavoriteSerializer, EventSerializer, UserGroupSerializer, GroupMemberSerializer, UserGroupCreateSerializer
from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, Achievement, UserAchievement, Task, Challenge, UserChallenge, UserTask, UserStat, Level, FormQuestion, UserAnswer, Advice, Guide, Favorite, Event, UserGroup, GroupMember
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
from rest_framework.views import APIView
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Prefetch
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        # username = request.data.get('username')
        # password = request.data.get('password')
        # user = User.objects.create(email=email, username=username)
        # user.set_password(password)
        # # user.email_confirmation_token = uuid.uuid4()
        # user.save()
        # # confirmation_link = f'http://127.0.0.1:8000/confirm-email/{user.email_confirmation_token}/'
        send_mail(
            'Подтверждение электронной почты',
            f'Пожалуйста, подтвердите вашу регистрацию, перейдя по следующей ссылке: ',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({
            'detail': 'Пожалуйста, проверьте свою почту для подтверждения регистрации.'
        }, status=status.HTTP_201_CREATED)

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_posted', 'category']

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
    
    @action(detail=False)
    def personal_vector(self, request):
        user_plans = UserPlan.objects.filter(user=self.request.user)
        habits_title = []
        for plan in user_plans:
            habits = UserHabit.objects.filter(plan=plan)
            for habit in habits:
                habit_title = habit.habit.title
                habits_title.append(habit_title)
        advices = Advice.objects.all()
        advices_text = []
        for advice in advices:
            advices_text.append(advice.description)
        vector = TfidfVectorizer()
        print(advices_text, habits_title)
        a_matrix = vector.fit_transform(advices_text).toarray()
        habits_matrix = vector.transform(habits_title).toarray()
        
        print("a_matrix shape:", a_matrix) 
         # Формат (количество документов advices_text, количество признаков)
        print("habits_matrix shape:", habits_matrix)  # Формат (количество документов habits_title, количество признаков)
        similar = cosine_similarity(a_matrix, habits_matrix)
        similar_indices = similar.argsort()[0][::-1]
        print("Рекомендуемые советы:")
        for index in similar_indices:
            print(f"- {advices_text[index]}")

    @action(detail=False)
    def search(self, request):
        query = request.GET.get('q', '')
        print(connection.vendor) 
        print(query)
        advices = []
        if query:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT a.title FROM eco_advice a
                        JOIN advice_search fts ON a.title = fts.title
                        WHERE advice_search MATCH %s
                    """, [query])
                advice_titles = [row[0] for row in cursor.fetchall()]
                print(advice_titles)
                advices = Advice.objects.filter(title__in=advice_titles)
                print(advices)
                advices_serializer = AdviceSerializer(advices, many=True, context={'request': request})
                return Response(advices_serializer.data)
    


class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_posted', 'category']

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
                if request.data['guide']:
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
    
    @action(detail=False)
    def advices(self, request):
        advices = Favorite.objects.filter(favorite_type='A')
        serializer = FavoriteSerializer(advices, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def guides(self, request):
        guides = Favorite.objects.filter(favorite_type='G')
        serializer = FavoriteSerializer(guides, many=True, context={'request': request})
        return Response(serializer.data)

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
    
class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer  

    def perform_destroy(self, instance):
        if instance.group.members.count() == 2:
            instance.group.delete()
        instance.delete()
        

class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserGroupSerializer  
        elif self.request.method == 'POST':
            return UserGroupCreateSerializer 
        return super().get_serializer_class() 

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('members')  

        for group in queryset:
            members = list(group.members.all())
            sorted_members = sorted(
                members,
                key=lambda member: member.member_stat.first().points if member.member_stat.exists() else 0,
                reverse=True
            )
            group.members.set(sorted_members)   
        return queryset.filter(members__user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid():
            user_group = UserGroup.objects.create(title = serializer.validated_data['title'])
            group_members = serializer.validated_data.get('members', [])
            for group_member in group_members:
                GroupMember.objects.create(user=group_member['user'], group=user_group, is_confirm=group_member['is_confirm'])
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)