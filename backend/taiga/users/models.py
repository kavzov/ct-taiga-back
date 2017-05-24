from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser


class User(User):
    def __str__(self):
        return "{id}. {fname} {lname}".format(id=self.id, fname=self.first_name, lname=self.last_name)

    class Meta:
        ordering = ['id']


# class User(AbstractBaseUser):
#     username = models.CharField(max_length=50)
#     email = models.EmailField(max_length=255, unique=True)
#     is_admin = models.BooleanField(null=False, blank=False, default=False)
#
#     def __str__(self):
#         return "{id}. {name}".format(id=self.id, name=self.username)
#
#     class Meta:
#         verbose_name = "user"
#         verbose_name_plural = "users"
#         ordering = ["id"]
#
#     USERNAME_FIELD = "username"
