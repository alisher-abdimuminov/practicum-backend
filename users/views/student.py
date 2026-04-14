import base64
from deepface import DeepFace
from datetime import datetime
from django.http import HttpRequest
from rest_framework import decorators
from shapely.geometry import Point, Polygon
from rest_framework.response import Response
from django.core.files.base import ContentFile

from ..models import AttendanceGroup, User, Attendance, Schedule
from ..serializers import AttendanceGroupSerializer, AreaSerializer, ScheduleSerializer


@decorators.api_view(http_method_names=["GET"])
def get_attendance_group(request: HttpRequest):
    now = datetime.now()
    student: User = request.user

    schedule = Schedule.objects.filter(
        groups=student.group, weekday=now.weekday()
    ).first()
    if not schedule:
        return Response({"status": "error", "code": "you_are_free", "data": None})

    print(schedule)
    print(now)

    a_group, _ = AttendanceGroup.objects.get_or_create(
        student=student, created__date=now.date()
    )

    return Response(
        {
            "status": "success",
            "code": "",
            "data": {"a_group": AttendanceGroupSerializer(a_group).data},
        }
    )


@decorators.api_view(http_method_names=["GET"])
def get_schedule(request: HttpRequest):
    student: User = request.user

    schedule = Schedule.objects.filter(groups=student.group)

    return Response(
        {
            "status": "success",
            "code": "",
            "data": {"schedule": ScheduleSerializer(schedule).data},
        }
    )


@decorators.api_view(http_method_names=["POST"])
def check_location(request: HttpRequest):
    now = datetime.now()
    student: User = request.user

    schedule = Schedule.objects.filter(
        groups=student.group, weekday=now.weekday()
    ).first()
    if not schedule:
        return Response({"status": "success", "code": "you_are_free", "data": None})

    try:
        user_lat = float(request.data.get("latitude"))
        user_lon = float(request.data.get("longitude"))
    except (TypeError, ValueError):
        return Response({"status": "error", "code": "invalid_coords", "data": None})

    user_point = Point(user_lat, user_lon)

    try:

        def extract_coords(coord_str):
            parts = coord_str.replace(" ", "").split(",")
            return float(parts[0]), float(parts[1])

        polygon_vertices = [
            extract_coords(schedule.area.coord1),
            extract_coords(schedule.area.coord2),
            extract_coords(schedule.area.coord3),
            extract_coords(schedule.area.coord4),
        ]

        polygon = Polygon(polygon_vertices)

        if polygon.contains(user_point):
            return Response(
                {
                    "status": "success",
                    "code": "success",
                    "data": AreaSerializer(schedule.area).data,
                }
            )

    except Exception as e:
        print("error while process location:", e)

    return Response({"status": "error", "code": "not_in_area", "data": None})


@decorators.api_view(http_method_names=["POST"])
def make_attendance(request: HttpRequest):
    now = datetime.now()
    student: User = request.user
    base64data = request.data.get("image")
    longitude = request.data.get("longitude")
    latitude = request.data.get("latitude")

    try:
        format, imgstr = base64data.split(";base64,")
        ext = format.split("/")[-1]
        base64image = ContentFile(
            base64.b64decode(imgstr),
            name=f"attendance_{student.id}_{now.strftime('%H%M%S')}.{ext}",
        )
    except Exception:
        return Response({"status": "error", "code": "invalid_image"})

    schedule = Schedule.objects.filter(
        groups=student.group, weekday=now.weekday()
    ).first()
    if not schedule:
        return Response({"status": "success", "code": "you_are_free", "data": None})

    a_group, _ = AttendanceGroup.objects.get_or_create(
        student=student, created__date=now.date()
    )

    step_attr = None
    if 8 <= now.hour < 10:
        step_attr = "step_1"
    elif 10 <= now.hour < 12:
        step_attr = "step_2"
    elif 12 <= now.hour < 14:
        step_attr = "step_3"

    if not step_attr:
        return Response({"status": "error", "code": "out_of_time_range"})

    current_step_obj = getattr(a_group, step_attr)
    if current_step_obj and current_step_obj.status == "arrived":
        return Response({"status": "error", "code": "already_verified", "data": None})

    attendance = Attendance.objects.create(
        student=student,
        image=base64image,
        area=schedule.area,
        status="processing",
        longitude=longitude,
        latitude=latitude,
    )

    setattr(a_group, step_attr, attendance)
    a_group.save(update_fields=[step_attr])

    try:
        result = DeepFace.verify(
            img1_path=student.photo.path,
            img2_path=attendance.image.path,
            enforce_detection=False,
        )

        if result.get("verified"):
            attendance.status = "arrived"
            attendance.save(update_fields=["status"])
            return Response({"status": "success", "code": "verified"})
        else:
            attendance.status = "failed"
            attendance.save(update_fields=["status"])
            return Response({"status": "error", "code": "not_verified"})

    except Exception as e:
        print(f"Verification error: {e}")
        attendance.status = "failed"
        attendance.save(update_fields=["status"])
        return Response({"status": "error", "code": "verification_system_error"})
