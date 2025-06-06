from rest_framework import serializers

from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, Achievement, UserAchievement, Challenge, Task, UserChallenge, UserTask, UserStat, Level, FormQuestion, UserAnswer, Advice, Guide, Favorite, Event, UserGroup, GroupMember

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ['url', 'id', 'title']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'is_active', 'role', 'username' ,'password','want_organization' ]
        extra_kwargs = {
            'password': {'write_only': True},
            # 'role': {'required': True}
        }
        depth = 1

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True


        if password is not None:
            instance.set_password(password)
        instance.save()

        UserStat.objects.create(user = instance)

        return instance


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'id', 'title']

class HabitSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(HabitSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Habit
        fields = '__all__'

class FormQuestionSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(FormQuestionSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = FormQuestion
        fields = ['id', 'url', 'title']

class FormSerializer(serializers.HyperlinkedModelSerializer):
    questions = FormQuestionSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super(FormSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Form
        fields = ['url', 'id', 'title', 'questions']

class UserAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'

class UserAchievementSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserAchievementSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = UserAchievement
        fields = '__all__'


class UserHabitSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserHabitSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2

    class Meta:
        model = UserHabit
        fields = ['url', 'id', 'habit', 'plan', 'status']

class UserPlanSerializer(serializers.HyperlinkedModelSerializer):
    habits = UserHabitSerializer(many=True, read_only=True)
    form = FormSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserPlanSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2

    class Meta:
        model = UserPlan
        fields = '__all__'

class AchievementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Achievement
        fields = ['url', 'id', 'title', 'description', 'icon']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TaskSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Task
        fields = '__all__'

class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    start_date = serializers.DateField(format='%d.%m.%Y')
    finish_date = serializers.DateField(format='%d.%m.%Y')

    def __init__(self, *args, **kwargs):
        super(ChallengeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Challenge
        fields = ['url', 'id', 'title', 'category', 'description', 'tasks', 'goal', 'achievement', 'status', 'start_date', 'finish_date', 'this_week', 'this_week_date']



class UserTaskSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserTaskSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = UserTask
        fields = ['url', 'id', 'task', 'challenge', 'status']

class UserChallengeSerializer(serializers.HyperlinkedModelSerializer):
    tasks = UserTaskSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserChallengeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2

    class Meta:
        model = UserChallenge
        fields = ['id', 'url', 'challenge','status', 'tasks']

class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'url', 'min_points', 'title', 'description']

class AchievementStatSerializer(serializers.Serializer):
    achievement = AchievementSerializer(many=False, read_only=True)  # Или укажите нужное поле
    count = serializers.IntegerField()

class UserStatSerializer(serializers.HyperlinkedModelSerializer):
    all_achievements = AchievementStatSerializer(many=True, read_only=True)
    next_level = LevelSerializer( read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserStatSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = UserStat
        fields = ['url', 'id', 'user', 'level', 'completed_plans', 'all_achievements', 'points', 'next_level', 'achievements_count']

class AdviceSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(AdviceSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Advice
        fields = ['id', 'url', 'title', 'description', 'category', 'icon', 'is_posted']

class GuideSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(GuideSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Guide
        fields = ['id', 'url', 'title', 'description', 'category', 'annotation', 'icon', 'is_posted']

class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(FavoriteSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Favorite
        fields = ['url', 'id', 'user', 'advice', 'guide', 'favorite_type']

class EventSerializer(serializers.HyperlinkedModelSerializer):
    event_date = serializers.DateField(format='%d.%m.%Y')

    class Meta:
        model = Event
        fields = ['url', 'id', 'user', 'title', 'description', 'event_date', 'status', 'report', 'report_image', 'afisha_image']

class GroupMemberSerializer(serializers.HyperlinkedModelSerializer):
    member_stat = UserStatSerializer(many=True, read_only=True)

    class Meta:
        model = GroupMember
        fields = ['url', 'user', 'group', 'is_confirm', 'member_stat']
        depth = 1

class GroupMemberCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['url', 'user', 'group', 'is_confirm']

class UserGroupSerializer(serializers.HyperlinkedModelSerializer):
    members = GroupMemberSerializer(many=True)

    class Meta:
        model = UserGroup
        fields = [ 'url', 'id', 'title', 'members']

class UserGroupCreateSerializer(serializers.HyperlinkedModelSerializer):
    members = GroupMemberCreateSerializer(many=True)

    class Meta:
        model = UserGroup
        fields = [ 'url', 'id', 'title', 'members']
