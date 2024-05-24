from .models import Hall
from rest_framework import serializers


class HallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hall
        fields = ["id", "teacher", "available", "attend_code", "is_closed"]
        extra_kwargs = {
            'attend_code': {'read_only': True},
            'x_room_id': {'read_only': True}
        }


class HallRetrieveSerialiezr(serializers.ModelSerializer):

    class Meta:
        model = Hall
        fields = ["teacher_id", "students", "attend_code", "x_room_id", "is_closed", "updated_at"]


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hall
        fields = ["teacher", "students", "attend_code"]
