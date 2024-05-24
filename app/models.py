from django.db import models

from account.models import User
from config.exceptions import OvercapacityOfStudents


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성 일시",
        help_text="데이터가 생성 된 날짜 입니다."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정 일시",
        help_text="데이터가 수정 된 날짜 입니다."
    )

    class Meta:
        abstract = True


class Hall(BaseModel):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', limit_choices_to={'status': User.TEACHER})
    students = models.ManyToManyField(User, related_name='students', limit_choices_to={'status': User.STUDENT}, blank=True)
    available = models.IntegerField(default=0, verbose_name='최대 참석 가능 수강생 인원')
    attend_code = models.CharField(max_length=8, verbose_name='강의장 참석을 위한 코드', default=0)
    x_room_id = models.CharField(max_length=16, verbose_name='강의장 ID', default=0)

    is_closed = models.BooleanField(default=True, verbose_name="강의장 종료")
        
    def save(self, *args, **kwargs):
        if self.attend_code in ['0', 0]:
            import random, string
            target = string.ascii_letters + string.digits
            self.attend_code = "".join(random.choices(target, k=5))  # 고유값 무작위 문자열
            self.x_room_id = "".join(random.choices(target, k=10))

            super().save(*args, **kwargs)
