from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

from .models import (
    Area,
    User,
    Attendance,
    Submit,
    Task,
)


admin.site.unregister(Group)

@admin.register(Group)
class GroupModelAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(Area)
class AreaModelAdmin(ModelAdmin):
    list_display = ["name", "coord1", "coord2", "coord3", "coord4" ]
    search_fields = ["name"]


@admin.register(Attendance)
class AttendanceModelAdmin(ModelAdmin):
    list_display = ["student", "status", "created", "area"]
    search_fields = ["student"]
    list_filter = ["student", "status", "created"]


@admin.register(Submit)
class SubmitModelAdmin(ModelAdmin):
    list_display = ["task", "student", "status", "point", "created"]
    list_filter = ["student", "status", "created", ]


@admin.register(Task)
class TaskModelAdmin(ModelAdmin):
    list_display = ["name", "teacher", "created", ]
    list_filter = ["teacher", "created", ]



@admin.register(User)
class UserModelAdmin(UserAdmin, ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ["username", "full_name", "email", "phone", ]
    search_fields = ["username", "full_name", "email", "phone", ]
    list_filter = ["group", "course"]
    model = User
    fieldsets = (
        ("Ma'lumotlar", {
            "fields": ("full_name", "phone", "group", "passport_number", "birth_date", "course",  "faculty", "payment_method", "gpa", "image", )
        }), 
    )
    add_fieldsets = (
         ("Yangi foydalanuvchi qo'shish", {
            "fields": ("username", "password1", "password2", "full_name", "phone", "group", "passport_number", "birth_date", "course",  "faculty", "payment_method", "gpa", "image", )
        }),
    )