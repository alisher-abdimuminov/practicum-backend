from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False)

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    group = models.CharField(max_length=100, null=True, blank=True)
    passport_number = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    gpa = models.FloatField(default=0)

    image = models.ImageField(
        upload_to="images/users", verbose_name="Rasm", null=True, blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

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
    name = models.CharField(max_length=100, verbose_name="Nomi")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'qituvchi")
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
    status = models.CharField(max_length=100, verbose_name="Holati")
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
    status = models.CharField(max_length=100, verbose_name="Holati")
    image = models.ImageField(upload_to="images/attendances", verbose_name="Rasm")

    created = models.DateTimeField(auto_now_add=True, verbose_name="O'tgan vaqti")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = "Davomat"
        verbose_name_plural = "Davomat"

