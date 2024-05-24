from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Hall
from account.models import User
from .serializers import HallSerializer, StudentSerializer, HallRetrieveSerialiezr
from config.exceptions import OvercapacityOfStudents, TerminatedHall, TakeYourOwnCourse, HallNotFound, X_USER_IDOrX_ROOM_IDNotFound


class HallViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

    # 강의장 개설 (강사)
    @swagger_auto_schema(operation_id="강의장 개설 (강사)")
    def create(self, request, *args, **kwargs):
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 강의장 종료 (강사)
    @swagger_auto_schema(
            operation_id="강의장 종료 (강사)",
            manual_parameters=[
                openapi.Parameter(
                    'X-ROOM-ID',
                    openapi.IN_HEADER,
                    description='X-ROOM-ID',
                    type=openapi.TYPE_STRING,
                    required=True
                ),
                openapi.Parameter(
                    'X-USER-ID',
                    openapi.IN_HEADER,
                    description='X-USER-ID',
                    type=openapi.TYPE_STRING,
                    required=True
                )
            ]
        )
    def destroy(self, request, *args, **kwargs):
        x_room_id = request.headers.get('X-ROOM-ID')
        x_user_id = request.headers.get('X-USER-ID')

        teacher_id = self.kwargs.get('pk', None)

        try:
            instance = Hall.objects.get(teacher_id=teacher_id)
        except Hall.DoesNotExist:
            raise HallNotFound
        
        user = User.objects.get(id=instance.teacher_id)

        if x_room_id == instance.x_room_id and x_user_id == user.x_user_id:
            Hall.objects.filter(teacher_id=teacher_id).update(is_closed=True)
            instance.refresh_from_db()

            return Response({
                "teacher_id": teacher_id,
                "is_closed": instance.is_closed
            }, status=status.HTTP_200_OK)
        else:
            raise X_USER_IDOrX_ROOM_IDNotFound
    
    # 강의장 조회 (공통)
    @swagger_auto_schema(
            operation_id="강의장 조회 (공통)",
            manual_parameters=[
                openapi.Parameter(
                    'X-ROOM-ID',
                    openapi.IN_HEADER,
                    description='X-ROOM-ID',
                    type=openapi.TYPE_STRING,
                    required=True
                ),
                openapi.Parameter(
                    'X-USER-ID',
                    openapi.IN_HEADER,
                    description='X-USER-ID',
                    type=openapi.TYPE_STRING,
                    required=True
                )
            ]
        )
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        hall = get_object_or_404(queryset, pk=pk)
        serializer = HallRetrieveSerialiezr(hall)

        x_user_id = request.headers.get('X-USER-ID')
        x_room_id = request.headers.get('X-ROOM-ID')

        instance = serializer.data

        target = [User.objects.get(id=i).x_user_id  for i in instance.get('students')]

        if x_user_id in target and x_room_id == instance.get('x_room_id', None):
            return Response(serializer.data)
        raise X_USER_IDOrX_ROOM_IDNotFound


class StudentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Hall.objects.all()
    serializer_class = StudentSerializer

    # 강의장 참석 (수강생)
    @swagger_auto_schema(
            operation_id="강의장 참석 (수강생)", 
            manual_parameters=[
                openapi.Parameter(
                    'X-USER-ID', 
                    openapi.IN_HEADER, 
                    description='X-USER-ID',
                    type=openapi.TYPE_STRING,
                    required=True
                    )
                ]
            )
    def create(self, request, *args, **kwargs):
        x_user_id = request.headers.get('X-USER-ID')

        teacher_id = request.data.get('teacher', None)
        student_ids = request.data.get('students', None)

        instance, created = Hall.objects.get_or_create(teacher_id=teacher_id)


        # TODO: 강의가 종료 되었다면 STOP
        if instance.is_closed == True:
            raise TerminatedHall

        # TODO: 강의 수강생 인원수가 available 을 넘었다면 STOP
        total_students = instance.students.count() + len(student_ids)
        if total_students > instance.available:
            raise OvercapacityOfStudents
        
        # TODO: 본인이 작성한 강의에 등록할 수 없습니다. STOP
        for index, student_id in enumerate(student_ids):
            if instance.teacher_id == student_id:
                raise TakeYourOwnCourse
            
            # TODO: 이미 참석 중 이라면 sttend_code
            if instance.students.filter(id=student_id).exists():
                # TODO: User 가지고 있는 X-USER-ID == request.headers.get('X-USER-ID') 비교
                if x_user_id == instance.students.get(id=student_id).x_user_id:
                    return Response({"attend_code": instance.attend_code})
                raise X_USER_IDOrX_ROOM_IDNotFound
            
            instance.students.add(student_ids[index])
          
        instance.save()
        serializer = StudentSerializer(instance)

        return Response(serializer.data)
