from rest_framework import serializers

from .models import (
    Area,
    User,
    Group,
    Schedule,
    Task,
    Submit,
)


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            "pk",
            "name",
            "coord1",
            "coord2",
            "coord3",
            "coord4",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "full_name",
            "phone",
            "group",
            "passport_number",
            "faculty",
            "payment_method",
            "gpa",
            "image",
            "role",
        )


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "full_name",
        )


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "full_name",
            "phone",
            "group",
            "level",
            "faculty",
            "payment_method",
            "gpa",
            "image",
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "pk",
            "name",
        )


class ScheduleSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(Group, many=True)
    area = AreaSerializer(Area)
    class Meta:
        model = Schedule
        fields = (
            "groups",
            "area",
            "weekday",
        )


class TaskSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    teacher = TeacherSerializer()
    class Meta:
        model = Task
        fields = (
            "pk",
            "name",
            "group",
            "teacher",
            "description",
            "created",
        )


class SubmitSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    task = TaskSerializer()
    class Meta:
        model = Submit
        fields = (
            "pk",
            "task",
            "student",
            "status",
            "point",
            "file",
            "created",
        )
