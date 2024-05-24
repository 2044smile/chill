from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_id, password, **extra_fields):
        if not user_id:
            raise ValueError('must have an user_id')
        if not password:
            raise ValueError('must have a password')
        
        user = self.model(
            user_id=user_id,
            password=password,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(user_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'

    STATUS_CHOICE = (
        (STUDENT, '수강생'),
        (TEACHER, '강사'),
        (ADMIN, '관리자')
    )
    user_id = models.CharField(
        verbose_name='user_id',
        max_length=32,
        unique=True
    )
    password = models.CharField(
        verbose_name='password',
        max_length=255,
    )
    status = models.CharField(
        verbose_name='회원 정보',
        max_length=16,
        choices=STATUS_CHOICE, 
    )
    x_user_id = models.CharField(
        verbose_name='회원 ID',
        max_length=16
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return self.user_id
        
    def save(self, *args, **kwargs):
        if self.x_user_id in ['0', 0, '']:
            import random, string
            target = string.ascii_letters + string.digits
            self.x_user_id = "".join(random.choices(target, k=10))

            super().save(*args, **kwargs)
