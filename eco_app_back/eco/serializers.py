from rest_framework import serializers

from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, Achievement, UserAchievement, Challenge, Task, UserChallenge, UserTask, UserStat, Level

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
        fields = ['id', 'url', 'email', 'is_active', 'role', 'username' ,'password', ]
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

class FormSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Form
        fields = ['url', 'id', 'title']

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

    def __init__(self, *args, **kwargs):
        super(UserPlanSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = UserPlan
        fields = '__all__'

class AchievementSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Achievement
        fields = ['url', 'id', 'title', 'description', 'icon']

class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ChallengeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Challenge
        fields = '__all__'

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
            self.Meta.depth = 1

    class Meta:
        model = UserChallenge
        fields = '__all__'

class LevelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Level
        fields = '__all__'

class UserStatSerializer(serializers.HyperlinkedModelSerializer):
    all_achievements = UserAchievementSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserStatSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2

    class Meta:
        model = UserStat
        fields = ['url', 'id', 'user', 'level', 'completed_plans', 'all_achievements', 'points']