from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from department.models import Department
from decorators.ClassDecorators import with_json_serialize

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(username=username)
        user.is_admin = False

        if password != None:
            user.set_password(password)

        return user


@with_json_serialize
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, default=None, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, default=None, null=True)
    position = models.CharField(max_length=100, default=None, null=True)
    email = models.CharField(max_length=255, default=None, null=True)
    telephone = models.CharField(max_length=15, default=None, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.fullname} [{self.position} -> {self.department}] ({self.id})"
