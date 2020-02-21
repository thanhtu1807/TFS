from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.ForeignKey('Role', related_name='role_user', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey('Group', related_name='group_user', on_delete=models.CASCADE, null=True)
    # email field is used as a username for authentication
    USERNAME_FIELD = 'email'
    # A list of the field names that will be prompted for when creating a user via the createsuperuser
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name']

    def __str__(self):
        return f'{self.email}'


class Role(models.Model):
    role_name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f'{self.role_name}'


class Group(models.Model):
    group_name = models.CharField(max_length=255, null=False, unique=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.group_name}'
