import requests
from django.apps import apps
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Hemis OAuth orqali kelgan URL rasmlarni yuklab ImageField-ga saqlaydi"

    def handle(self, *args, **options):
        Student = apps.get_model("users", "user")

        students = Student.objects.filter(role="student")

        total = students.count()
        self.stdout.write(self.style.SUCCESS(f"{total} ta rasm yuklanishi kerak."))

        for index, student in enumerate(students, 1):
            try:
                response = requests.get(student.image, timeout=15)

                if response.status_code == 200:
                    ext = ".jpg"
                    if "png" in student.image.lower():
                        ext = ".png"

                    file_name = f"student_{student.id}{ext}"

                    student.photo.save(
                        file_name, ContentFile(response.content), save=True
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[{index}/{total}] Yuklandi: ID {student.id}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"[{index}/{total}] Xato status {response.status_code}: ID {student.id}"
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"[{index}/{total}] Xatolik ID {student.id}: {str(e)}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Jarayon yakunlandi!"))
