from django.urls import path

from .views.auth import (
    login,
    profile,
    callback,
)
from .views.admin import (
    get_areas,
    add_area,
    get_students,
    get_groups,
    get_schedules,
    get_teacher_submits,
    get_teacher_tasks,
    get_student_submits,
    get_student_tasks,
    add_task,
)


urlpatterns = [
    path("auth/hemis/callback/", callback),
    path("auth/login/", login),
    path("profile/", profile),
    path("admin/areas/", get_areas),
    path("admin/areas/add/", add_area),
    path("admin/students/", get_students),
    path("admin/groups/", get_groups),
    path("admin/schedules/", get_schedules),
    path("teacher/tasks/", get_teacher_tasks),
    path("teacher/tasks/add/", add_task),
    path("teacher/submits/", get_teacher_submits),
    path("student/tasks/", get_student_tasks),
    path("student/submits/", get_student_submits),
]
