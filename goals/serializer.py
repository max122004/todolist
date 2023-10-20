from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User
from goals.models import GoalCategory, Goal


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'update', 'user')
        fields = '__all__'

    def validated_data(self, value):
        if value.is_dalated:
            raise ValidationError('not allowed')
        if value.user != self.context['request'].user:
            raise ValidationError('not owner')

        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'update', 'user')


class GoalListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'update', 'user')


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'update', 'user')


class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'update', 'user')
        fields = '__all__'

        def validated_data(self, value):
            if value.is_dalated:
                raise ValidationError('not allowed')
            if value.user != self.context['request'].user:
                raise ValidationError('not owner')

            return value