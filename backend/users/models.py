from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin,)
from django.core.validators import MinLengthValidator
from django.db.models import BooleanField, CharField, EmailField


class UserManager(BaseUserManager):
    """
    Менеджер для создания пользователей
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Для Superuser должно быть указано is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Для Superuser must должно быть указано is_superuser=True.'
            )
        return self._create_user(email, password, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    email = EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        db_index=True,
        unique=True,
        validators=[MinLengthValidator(settings.EMAIL_MIN_LENGTH)],
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.'}
    )

    password = CharField(
        'Пароль',
        max_length=settings.PASSWORD_MAX_LENGTH,
        validators=[MinLengthValidator(settings.PASSWORD_MIN_LENGTH)],
        help_text='Введите пароль',
    )
    is_staff = BooleanField(
        'Staff status',
        default=False,
    )
    is_superuser = BooleanField(
        'Admin status',
        default=False,
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'User: {self.email}'
