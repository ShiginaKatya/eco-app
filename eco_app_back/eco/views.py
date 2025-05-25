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
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
import numpy as np
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, BasePermission
from django.utils import timezone
from .utils import personal_advices
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect


class IsOrganization(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.title == 'Организация'

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['want_organization']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_token = default_token_generator.make_token(user)
            confirm_link = f"{request.build_absolute_uri('/api/users/confirm_email')}?uid={uid}&confirm_token={confirm_token}"

            send_mail(
                'Регистрация в веб-приложении ECO Green Free',
                f'Перейдите по ссылке для подтверждения регистрации: {confirm_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            return Response({'title': 'Пользователь создан, подтвердите email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def confirm_email(self, request):
        uidb64 = request.query_params.get('uid')
        confirm_token = request.query_params.get('confirm_token')
        if uidb64 and confirm_token:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, confirm_token):
                user.is_email_confirmed = True
                user.save()
                return redirect('http://localhost:5173/login/')
            return Response({'title': 'Некорректная или устаревшая ссылка.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'title': 'Некорректная или устаревшая ссылка.'}, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            if ('want_organization' in request.data) and (request.data['want_organization'] == False):
                if 'role' in request.data:
                    send_mail(
                        'Ваша учетная запись была изменена. Eco Green Life',
                        f'Аккаунт теперь представляет собой организацию. Можете воспользоваться предоставленным функционалом',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                else:
                    send_mail(
                        'Заявка на создание аккаунта организации была отменена. Eco Green Life',
                        f'Можете повторить попытку или уточнить проблему по почте отправителя',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
                
                

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
    permission_classes = [IsAdminOrReadOnly]

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
    # permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['this_week']


    def get_queryset(self):
        challenges = Challenge.objects.all()
        for challenge in challenges:
            challenge.get_week()
            challenge.get_status()
        return challenges
    
    def partial_update(self, request, pk=None):
        challenge = get_object_or_404(Challenge, pk=pk)
        serializer = ChallengeSerializer(challenge, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            if ('this_week' in request.data) and (request.data['this_week'] == True):
                challenge.this_week_date = timezone.now()
                challenge.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrReadOnly]

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
                # challenge_serializer = UserChallengeSerializer(challenge, context={'request': request})
                if challenge.challenge.id == serializer.validated_data['challenge'].id:
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
    permission_classes = [IsAdminOrReadOnly]

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

    # @action(detail=False)
    # def personal(self, request):
    #     user_plans = UserPlan.objects.filter(user=self.request.user)
    #     habits_category = []
    #     for plan in user_plans:
    #         habits = UserHabit.objects.filter(plan=plan)
    #         for habit in habits:
    #             habit_category = habit.habit.category.title
    #             habits_category.append(habit_category)
    #     user_challenges = UserChallenge.objects.filter(user = self.request.user)
    #     challenges_category = []
    #     for challenge in user_challenges:
    #         challenge_category = challenge.challenge.category.title
    #         challenges_category.append(challenge_category)
    #     user_categories = habits_category + challenges_category
    #     categories = Category.objects.all()
    #     use_categories = {}
    #     for category in categories:
    #         use_categories[category] = user_categories.count(category.title)
    #     use_categories = sorted(use_categories.items(), key=lambda item: item[1])[:2]
    #     personal_advices = Advice.objects.filter(Q(category = use_categories[0][0]) | Q(category = use_categories[1][0]))
    #     random_advices = personal_advices.order_by('?')[:3]
    #     personal_serializer = AdviceSerializer(random_advices, many=True, context={'request': request})
    #     print(random_advices)
    #     return Response(personal_serializer.data)
    
    @action(detail=False)
    def personal_vector(self, request):
        based_advices, opposite_advices  = personal_advices(self.request.user)
        if based_advices and opposite_advices:
            based_serializer = AdviceSerializer(based_advices, many=True, context={'request': request})
            opposite_serializer = AdviceSerializer(opposite_advices, many=True, context={'request': request})
            return Response({'based_advices': based_serializer.data,'opposite_advices': opposite_serializer.data}, status=status.HTTP_200_OK)
        else:
            random_advices = Advice.objects.order_by('?')[:3]
            random_serializer = AdviceSerializer(random_advices, many=True, context={'request': request})
            return Response({'random_advices': random_serializer.data}, status=status.HTTP_200_OK)


    @action(detail=False)
    def search(self, request):
        query = request.GET.get('q', '')
        print(connection.vendor) 
        print(query)
        advices = []
        if query:
            with connection.cursor() as cursor:
                cursor.execute("SELECT eco_advice.title  FROM eco_advice JOIN advice_search fts ON eco_advice.title = fts.title WHERE advice_search MATCH %s", [query])
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
                # favorite_serializer = FavoriteSerializer(favorite, context={'request': request})
                if request.data['advice']:
                    if favorite.advice.id == serializer.validated_data['advice'].id:
                        return Response({'title': 'Совет уже добавлен'}, status=status.HTTP_400_BAD_REQUEST)
                        break
                if request.data['guide']:
                    if favorite.guide.id == serializer.validated_data['guide'].id:
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
    permission_classes = [IsOrganization]

    def get_queryset(self):
        events = Event.objects.filter(user=self.request.user).order_by('event_date')
        for event in events:
            event.get_status()
        return events
    
    def partial_update(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            if 'event_date' in request.data and event.event_date != serializer.validated_data['event_date']:
                event.status = 'Перенесено'
            else:
                event.status = 'Назначено'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
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
        serializer = UserGroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            user_group = UserGroup.objects.create(title = serializer.validated_data['title'])
            group_members = serializer.validated_data.get('members', [])
            for group_member in group_members:
                print(group_member['user'])
                GroupMember.objects.create(user=group_member['user'], group=user_group, is_confirm=group_member['is_confirm'])
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)