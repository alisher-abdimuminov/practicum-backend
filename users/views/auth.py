from decouple import config
from django.http import HttpRequest
from rest_framework import decorators
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from ..client import HemisClient
from ..models import User, Group
from ..serializers import UserSerializer, TeacherSerializer, StudentSerializer


CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
REDIRECT_URI = config("REDIRECT_URI")

STUDENT_AUTHORIZE_URL = config("STUDENT_AUTHORIZE_URL")
STUDENT_ACCESS_TOKEN_URL = config("STUDENT_ACCESS_TOKEN_URL")
STUDENT_RESOURCE_OWNER_URL = config("STUDENT_RESOURCE_OWNER_URL")

TEACHER_AUTHORIZE_URL = config("TEACHER_AUTHORIZE_URL")
TEACHER_ACCESS_TOKEN_URL = config("TEACHER_ACCESS_TOKEN_URL")
TEACHER_RESOURCE_OWNER_URL = config("TEACHER_RESOURCE_OWNER_URL")

hemis_student_client = HemisClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    authorize_url=STUDENT_AUTHORIZE_URL,
    access_token_url=STUDENT_ACCESS_TOKEN_URL,
    resource_owner_url=STUDENT_RESOURCE_OWNER_URL
)

hemis_teacher_client = HemisClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    authorize_url=TEACHER_AUTHORIZE_URL,
    access_token_url=TEACHER_ACCESS_TOKEN_URL,
    resource_owner_url=TEACHER_RESOURCE_OWNER_URL
)


@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username:
        return Response(
            {
                "status": "error",
                "code": "400",
                "data": "Foydalanuvch nomi majburiy",
            }
        )

    if not password:
        return Response(
            {
                "status": "error",
                "code": "400",
                "data": "Kalit so'z maydoni majburiy",
            }
        )

    user = User.objects.filter(username=username)

    if not user:
        return Response(
            {"status": "error", "code": "404", "data": "Foydalanuvchi nomi topilmadi"}
        )

    user = user.first()

    if not user.check_password(raw_password=password):
        return Response(
            {
                "status": "error",
                "code": "400",
                "data": "Kalit so'z mos kelmadi",
            }
        )
    
    token = Token.objects.get_or_create(user=user)

    return Response({
        "status": "success",
        "code": "200",
        "data": {
            **UserSerializer(user).data,
            "token": token[0].key
        }
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def profile(request: HttpRequest):
    user = request.user
    token = Token.objects.get_or_create(user=user)
    return Response({
        "status": "success",
        "code": "200",
        "data": {
            **UserSerializer(user).data,
            "token": token[0].key
        }
    })


@decorators.api_view(http_method_names=["POST"])
def callback(request: HttpRequest):
    code = request.data.get("code")
    type = request.data.get("type")
    client = None


    if type == "teacher":
        client = hemis_teacher_client
    else:
        client = hemis_student_client

    access_token_response = client.get_access_token(code)
    print(access_token_response)

    if "access_token" in access_token_response:
        access_token = access_token_response.get("access_token")

        user_details = client.get_user_details(access_token=access_token)

        if user_details:
            if type == "teacher":
                username = user_details.get("login")

                teacher = User.objects.filter(username=username)
                print(user_details)

                if teacher:
                    teacher = teacher.first()
                    teacher.full_name = user_details.get("name")
                    teacher.image = user_details.get("picture_full")
                    teacher.birth_date = user_details.get("birth_date")
                    teacher.phone = user_details.get("phone")
                    teacher.passport_number = user_details.get("passport_number")
                    teacher.role = "teacher"
                    teacher.save()

                    token = Token.objects.get_or_create(user=teacher)

                    return Response({
                        "status": "success",
                        "code": "200",
                        "data": {
                            **UserSerializer(teacher).data,
                            "token": token[0].key
                        }
                    })
                else:
                    teacher = User.objects.create(
                        username=username,
                        full_name=user_details.get("name"),
                        image=user_details.get("picture_full"),
                        birth_date=user_details.get("birth_date"),
                        phone=user_details.get("phone"),
                        passport_number=user_details.get("passport_number"),
                        role="teacher"
                    )

                    token = Token.objects.get_or_create(user=teacher)

                    return Response({
                        "status": "success",
                        "code": "200",
                        "data": {
                            **UserSerializer(teacher).data,
                            "token": token[0].key
                        }
                    })
            else:
                username = user_details.get("student_id_number")

                student = User.objects.filter(username=username)

                group = Group.objects.filter(name=user_details.get("data", {}).get("group").get("name"))
                if not group:
                    group = Group.objects.create(
                        name=user_details.get("data", {}).get("group").get("name")
                    )
                else:
                    group = group.first()

                if student:
                    student = student.first()

                    student.full_name = user_details.get("name")
                    student.phone = user_details.get("phone")
                    student.passport_number = user_details.get("passport_number")
                    student.image = user_details.get("picture_full")
                    student.birth_date = user_details.get("birth_date")
                    student.group = group
                    student.level = user_details.get("data", {}).get("level", {}).get("name")
                    student.payment_method = user_details.get("data", {}).get("paymentForm", {}).get("name")
                    student.faculty = user_details.get("data", {}).get("faculty", {}).get("name")
                    student.gpa = user_details.get("data", {}).get("avg_gpa")
                    student.save()

                    token = Token.objects.get_or_create(user=student)

                    return Response({
                        "status": "success",
                        "code": "200",
                        "data": {
                            **UserSerializer(student).data,
                            "token": token[0].key
                        }
                    })
                else:
                    student = User.objects.create(
                        username=username,
                        full_name=user_details.get("name"),
                        phone=user_details.get("phone"),
                        passport_number=user_details.get("passport_number"),
                        image=user_details.get("picture_full"),
                        birth_date=user_details.get("birth_date"),
                        group=group,
                        faculty=user_details.get("data", {}).get("faculty", {}).get("name"),
                        payment_method=user_details.get("data", {}).get("paymentForm", {}).get("name"),
                        level=user_details.get("data", {}).get("level", {}).get("name"),
                        gpa=user_details.get("data", {}).get("avg_gpa")
                    )

                    token = Token.objects.get_or_create(user=student)

                    return Response({
                        "status": "success",
                        "code": "200",
                        "data": {
                            **UserSerializer(student).data,
                            "token": token[0].key
                        }
                    })
    return Response({
        "status": "error",
        "code": "200",
        "data": "Xatolik"
    })