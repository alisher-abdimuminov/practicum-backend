from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


ROLE = (
    ("admin", "Admin"),
    ("marketing", "Marketing"),
    ("teacher", "O'qituvchi"),
    ("student", "Talaba"),
)

SUBMIT_STATUS = (
    ("uploaded", "Yuklangan"),
    ("marked", "Baholangan"),
    ("rejected", "Qaytarilgan"),
)

ATTENDANCE_STATUS = (
    ("arrived", "Kelgan"),
    ("failed", "Xatolik"),
    ("processing", "Jarayonda"),
)


class Group(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Guruh nomi")
    teacher = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="group_teacher",
        limit_choices_to={"role": "teacher"},
        verbose_name="Amaliyot o'qituvchisi",
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False)

    full_name = models.CharField(max_length=100, verbose_name="To'liq ismi")
    phone = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Telefon raqami"
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Guruhi"
    )
    passport_number = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Passport raqami"
    )
    birth_date = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Tug'ilgan sanasi"
    )
    level = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Kursi"
    )
    faculty = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Fakulteti"
    )
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    gpa = models.FloatField(default=0, verbose_name="GPA si")

    image = models.CharField(
        max_length=1000, null=True, blank=True, verbose_name="Rasmi"
    )
    photo = models.ImageField(upload_to="students/", null=True, blank=True)

    role = models.CharField(
        max_length=100, choices=ROLE, default="student", verbose_name="Roli"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.full_name if self.full_name else self.username

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"


class Area(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    coord1 = models.CharField(max_length=100, verbose_name="Kordinata 1")
    coord2 = models.CharField(max_length=100, verbose_name="Kordinata 2")
    coord3 = models.CharField(max_length=100, verbose_name="Kordinata 3")
    coord4 = models.CharField(max_length=100, verbose_name="Kordinata 4")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Joylashuv"
        verbose_name_plural = "Joylashuvlar"


class Task(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nomi")
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="O'qituvchi"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Tavsifi")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Topshiriq"
        verbose_name_plural = "Topshiriqlar"


class Submit(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Topshiriq")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Talaba")
    status = models.CharField(
        max_length=100, choices=SUBMIT_STATUS, verbose_name="Holati"
    )
    point = models.IntegerField(default=5, verbose_name="Ball")
    file = models.FileField(upload_to="files/submits", verbose_name="Fayl")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqti")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.name

    class Meta:
        verbose_name = "Topshirma"
        verbose_name_plural = "Topshirmalar"


class Attendance(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Talaba")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Joylashuv")
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    status = models.CharField(
        max_length=100, choices=ATTENDANCE_STATUS, verbose_name="Holati"
    )
    image = models.ImageField(upload_to="images/attendances", verbose_name="Rasm")

    created = models.DateTimeField(auto_now_add=True, verbose_name="O'tgan vaqti")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Davomat"
        verbose_name_plural = "Davomat"


class AttendanceGroup(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Talaba")

    step_1 = models.ForeignKey(
        Attendance,
        related_name="step_1",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    step_2 = models.ForeignKey(
        Attendance,
        related_name="step_2",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    step_3 = models.ForeignKey(
        Attendance,
        related_name="step_3",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name="O'tgan vaqti")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)


class Schedule(models.Model):
    WEEK_DAY = (
        (0, "Dushanba"),
        (1, "Seshanba"),
        (2, "Chorshanba"),
        (3, "Payshanba"),
        (4, "Juma"),
        (5, "Shanba"),
        (6, "Yakshanba"),
    )

    groups = models.ManyToManyField(Group, related_name="schedule_groups")
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEK_DAY)

    def __str__(self):
        return self.get_weekday_display()
