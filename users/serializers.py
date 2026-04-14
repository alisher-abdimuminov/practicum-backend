from datetime import datetime
from rest_framework import serializers

from .models import (
    Area,
    User,
    Group,
    Schedule,
    Task,
    Submit,
    Attendance,
    AttendanceGroup,
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


class AttendanceSerializer(serializers.ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Attendance
        fields = (
            "student",
            "status",
            "area",
            "created",
        )


class AttendanceGroupSerializer(serializers.ModelSerializer):
    step_1 = serializers.SerializerMethodField()
    step_2 = serializers.SerializerMethodField()
    step_3 = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceGroup
        fields = (
            "student",
            "step_1",
            "step_2",
            "step_3",
        )

    def get_step_info(self, obj, step_num, start_h, end_h):
        attendance = getattr(obj, f"step_{step_num}")
        now = datetime.now()

        is_available = start_h <= now.hour < end_h

        is_past = now.hour >= end_h
        has_arrived = attendance is not None and attendance.status == "arrived"

        is_arrived = None
        if has_arrived:
            is_arrived = True
        elif is_past:
            is_arrived = False

        if attendance:
            return {
                "created": attendance.created.strftime("%Y-%m-%d %H:%M:%S"),
                "status": attendance.status,
                "is_available": is_available and attendance.status != "arrived",
                "is_arrived": is_arrived,
            }
        else:
            return {
                "created": None,
                "status": None,
                "is_available": is_available,
                "is_arrived": is_arrived,
            }

    def get_step_1(self, obj):
        return self.get_step_info(obj, 1, 8, 10)

    def get_step_2(self, obj):
        return self.get_step_info(obj, 2, 10, 12)

    def get_step_3(self, obj):
        return self.get_step_info(obj, 3, 12, 14)


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
