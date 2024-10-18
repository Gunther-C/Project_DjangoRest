from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

from django.utils import timezone
from datetime import date, datetime, timedelta
from django.db import models, IntegrityError


def validate_age(value):
    if value < 16:
        raise ValidationError('L\'âge minimum est de 16 ans.')


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):

        try:
            if 'age' not in extra_fields:
                raise ValueError('L\'âge minimum est de 16 ans insiste pas! MDR')
            validate_age(extra_fields['age'])
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            #user.save()
            return user
        except IntegrityError as e:
            raise ValueError("Ce nom d\'utilisateur est déja pris.")
        except ValidationError as e:
            raise ValueError(f"Les données fournies ne sont pas valides : {e.message}")

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    age = models.IntegerField(validators=[validate_age])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['age']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return f"{self.user} profile"
