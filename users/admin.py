from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
)

from .models import (
    Area,
    User,
    Attendance,
    AttendanceGroup,
    Submit,
    Task,
    Group as GGroup,
    Schedule,
)


admin.site.unregister(Group)


@admin.register(Group)
class GroupModelAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal = ("permissions",)


@admin.register(Area)
class AreaModelAdmin(ModelAdmin):
    list_display = ["name", "coord1", "coord2", "coord3", "coord4"]
    search_fields = ["name"]


@admin.register(Attendance)
class AttendanceModelAdmin(ModelAdmin):
    list_display = ["student", "status", "created", "area"]
    search_fields = ["student"]
    list_filter = ["student", "status", "created"]


@admin.register(AttendanceGroup)
class AttendanceGroupModelAdmin(ModelAdmin):
    list_display = ["student", "created"]
    search_fields = ["student"]
    list_filter = ["student", "created"]


@admin.register(Submit)
class SubmitModelAdmin(ModelAdmin):
    list_display = ["task", "student", "status", "point", "created"]
    list_filter = (
        ["student", AutocompleteSelectFilter],
        "status",
        "created",
    )
    list_filter_submit = True
    search_fields = ["name"]
    autocomplete_fields = (
        "task",
        "student",
    )


@admin.register(Task)
class TaskModelAdmin(ModelAdmin):
    list_display = (
        "name",
        "teacher",
        "group",
        "created",
    )
    list_filter = (
        ["teacher", AutocompleteSelectFilter],
        "created",
    )
    list_filter_submit = True
    search_fields = ["name"]
    autocomplete_fields = (
        "teacher",
        "group",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            if not request.user.is_superuser:
                kwargs["queryset"] = GGroup.objects.filter(teacher=request.user)
            else:
                kwargs["queryset"] = GGroup.objects.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk and not request.user.is_superuser:
            obj.teacher = request.user
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserModelAdmin(UserAdmin, ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = [
        "username",
        "full_name",
        "email",
        "phone",
        "role",
    ]
    search_fields = [
        "username",
        "full_name",
        "email",
        "phone",
    ]
    list_filter = (
        ["group", AutocompleteSelectFilter],
        "level",
        "role",
    )
    list_filter_submit = True
    autocomplete_fields = ("group",)
    model = User
    fieldsets = (
        (
            "Ma'lumotlar",
            {
                "fields": (
                    "groups",
                    "is_staff",
                    "full_name",
                    "phone",
                    "group",
                    "passport_number",
                    "birth_date",
                    "level",
                    "faculty",
                    "payment_method",
                    "gpa",
                    "image",
                    "role",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Yangi foydalanuvchi qo'shish",
            {
                "fields": (
                    "groups",
                    "is_staff",
                    "username",
                    "password1",
                    "password2",
                    "full_name",
                    "phone",
                    "group",
                    "passport_number",
                    "birth_date",
                    "level",
                    "faculty",
                    "payment_method",
                    "gpa",
                    "image",
                    "role",
                )
            },
        ),
    )


@admin.register(GGroup)
class GGroupModelAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    autocomplete_fields = ("teacher",)


@admin.register(Schedule)
class ScheduleModelAdmin(ModelAdmin):
    list_display = ["area", "weekday"]
    search_fields = ["name"]
    filter_horizontal = ("groups",)
    autocomplete_fields = ("area",)
