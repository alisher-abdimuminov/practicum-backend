from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response

from ..models import (
    Area,
    User,
    Group,
    Schedule,
    Task,
    Submit,
)
from ..serializers import (
    AreaSerializer,
    StudentSerializer,
    GroupSerializer,
    ScheduleSerializer,
    TaskSerializer,
    SubmitSerializer,
)


@decorators.api_view(http_method_names=["GET"])
def get_areas(request: HttpRequest):
    areas = Area.objects.all().order_by("-id")
    areas_serializer = AreaSerializer(areas, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": areas_serializer.data
    })


@decorators.api_view(http_method_names=["POST"])
def add_area(request: HttpRequest):
    data = request.data
    area_serializer = AreaSerializer(data=data)

    if area_serializer.is_valid():
        area_serializer.save()

        return Response({
            "status": "success",
            "code": "200",
            "data": None
        })
    
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })


@decorators.api_view(http_method_names=["GET"])
def get_students(request: HttpRequest):
    students = User.objects.filter(role="student").order_by("-id")
    student_serializer = StudentSerializer(students, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": student_serializer.data
    })


@decorators.api_view(http_method_names=["GET"])
def get_groups(request: HttpRequest):
    groups = Group.objects.all().order_by("-id")
    groups_serializer = GroupSerializer(groups, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": groups_serializer.data
    })


@decorators.api_view(http_method_names=["GET"])
def get_schedules(request: HttpRequest):
    schedules = Schedule.objects.all().order_by("-id")
    schedules_serializer = ScheduleSerializer(schedules, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": schedules_serializer.data
    })


@decorators.api_view(http_method_names=["GET"])
def get_teacher_tasks(request: HttpRequest):
    teacher = request.user
    tasks = Task.objects.filter(teacher=teacher).order_by("-id")
    tasks_serializer = TaskSerializer(tasks, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": tasks_serializer.data
    })


@decorators.api_view(http_method_names=["POST"])
def add_task(request: HttpRequest):
    teacher = request.user
    name = request.data.get("name")
    description = request.data.get("description")
    group = request.data.get("group")

    group = Group.objects.get(pk=group)

    Task.objects.create(
        name=name,
        teacher=teacher,
        group=group,
        description=description,
    )

    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })

@decorators.api_view(http_method_names=["GET"])
def get_teacher_submits(request: HttpRequest):
    teacher = request.user
    submits = Submit.objects.filter(task__teacher=teacher).order_by("-id")
    submits_serializer = SubmitSerializer(submits, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": submits_serializer.data
    })


@decorators.api_view(http_method_names=["GET"])
def get_student_tasks(request: HttpRequest):
    student = request.user
    tasks = Task.objects.filter(group=student.group).order_by("-id")
    tasks_serializer = TaskSerializer(tasks, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": tasks_serializer.data
    })


@decorators.api_view(http_method_names=["GET"])
def get_student_submits(request: HttpRequest):
    student = request.user
    submits = Submit.objects.filter(student=student).order_by("-id")
    submits_serializer = SubmitSerializer(submits, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": submits_serializer.data
    })
