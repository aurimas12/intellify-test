from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            # first_name, last_name,
            email, password=password

        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class Organization(models.Model):

    name = models.CharField(max_length=124, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(UserAccount)


class Project(models.Model):
    title = models.CharField(max_length=124, null=True, blank=True)
    description = models.TextField(blank=True)
    owner = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class OrganizationObject(models.Model):
    name = models.CharField(max_length=124)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectTeam(models.Model):
    ROLE_ADMIN = 1
    ROLE_MODERATOR = 2
    ROLE_SIMPLE_USER = 3

    ROLE = (
        (ROLE_ADMIN, ("Admin")),
        (ROLE_MODERATOR, ("Moderator")),
        (ROLE_SIMPLE_USER, ("Simple User")),
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE)
    created_date = models.DateTimeField(auto_now_add=True)


class DataPoint(models.Model):
    name = models.CharField(max_length=124, null=True, blank=True)
    object = models.ForeignKey(OrganizationObject, on_delete=models.CASCADE)
    value = models.FloatField()
    project_name = models.CharField(
        default='project name', max_length=124, null=True, blank=True)
    object_name = models.CharField(
        default='object name', max_length=124, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self) -> str:
    #     return self.created_date


class Configuration(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    data = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class TimeSeries(models.Model):
    data = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
