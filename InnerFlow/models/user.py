from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

# UserManager : 사용자 생성 로직을 정의하는 커스텀 매니저 클래스
class UserManager(BaseUserManager):
    # 일반 사용자 생성을 위한 메소드
    def create_user(self, kakao_id, password=None, **extra_fields):
        if not kakao_id:
            raise ValueError('The Kakao ID must be set') # 카카오 ID x -> 예외 발생
        user = self.model(kakao_id=kakao_id, **extra_fields) # user 모델 인스턴스 생성
        user.set_password(password) # 비밀번호 해싱하여 설정
        user.save(using=self._db) # db에 저장
        return user

    # 슈퍼유저(관리자) 생성을 위한 메서드
    def create_superuser(self, kakao_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True) # 권리자 권한
        extra_fields.setdefault('is_superuser', True) # 슈퍼유저 권한 설정

        return self.create_user(kakao_id, password, **extra_fields)

# User 모델
class User(AbstractBaseUser, PermissionsMixin):
    kakao_id = models.CharField(max_length=255, unique=True) # 사용자 고유 kakao ID
    profile = models.CharField(max_length=500, blank=True) # 사용자 프로필 정보
    nickname = models.CharField(max_length=50, blank=True) # 사용자 닉네임
    is_active = models.BooleanField(default=True) # 계정 활성 상태
    is_staff = models.BooleanField(default=False) # 관리자 권한 여부

    # Django의 기본 그룹 기능을 사용하기 위한 필드
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # UserMangage를 기본 매니저로 사용
    objects = UserManager()

    USERNAME_FIELD = 'kakao_id' # 로그인 시 사용될 필드 지정
    REQUIRED_FIELDS = [] # 슈퍼 유저 생성시 추가로 필요한 필드 목록

    def __str__(self):
        return str(self.kakao_id) # User 객체를 문자열로 변환할 때 kakao id를 반환
