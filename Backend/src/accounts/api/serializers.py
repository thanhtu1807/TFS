from rest_framework import serializers
from ..models import User, Role, Group, Function, Topic_present, Criteria, Appraisal, Appraisal_format, Session


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'password', 'role', 'group', 'created_at')
        extra_kwargs = {'password': {'write_only': True},
                        }

    # Override method create/update to hash password stored in DB
    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.role = validated_data.get('role', instance.role)
        instance.group = validated_data.get('group', instance.group)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'role_name')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'group_name', 'parent_group')


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ('id', 'function_name', 'role')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic_present
        fields = ('id', 'topic_name', 'description')


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ('id', 'criteria_name')


class AppraisalFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appraisal_format
        fields = ('id', 'format_name', 'criteria')


class AppraisalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appraisal
        fields = ('id', 'session', 'attendee', 'criteria', 'score', 'comment')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'presenter', 'topic', 'appraisal_format', 'date', 'deadline')
