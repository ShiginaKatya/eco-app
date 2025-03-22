from rest_framework import serializers

from .models import User, Role

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

    