from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )

        # Assign Admin Team group
        team_group = Group.objects.get(name='Admin')
        user.groups.set([team_group])

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250, unique=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=(
            ("MALE", "Male"),
            ("FEMALE", "Female"),
            ("OTHER", "Other"),
        ),
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email
