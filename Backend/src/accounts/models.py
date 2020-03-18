from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey('Role', related_name='role_user', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey('Group', related_name='group_user', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True, editable=False)
    # email field is used as a username for authentication
    USERNAME_FIELD = 'email'
    # A list of the field names that will be prompted for when creating a user via the createsuperuser
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    objects = UserManager()


class Role(models.Model):
    role_name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f'{self.role_name}'


class Group(models.Model):
    group_name = models.CharField(max_length=255, null=False, unique=True)
    parent_group = models.ForeignKey('self', related_name='groups', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.group_name}'


class Function(models.Model):
    function_name = models.CharField(max_length=255, null=False, unique=True)
    role = models.ManyToManyField('Role', related_name='role_function', null=True, blank=True)

    def __str__(self):
        return f'{self.function_name}'


class Topic_present(models.Model):
    topic_name = models.CharField(max_length=255, null=False, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.topic_name}'


class Criteria(models.Model):
    criteria_name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f'{self.criteria_name}'


class Appraisal_format(models.Model):
    format_name = models.CharField(max_length=255, null=False)
    criteria = models.ManyToManyField('Criteria', null=True, blank=True)

    def __str__(self):
        return f'{self.format_name}'


class Session(models.Model):
    presenter = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey('Topic_present', on_delete=models.CASCADE, null=True, blank=True)
    appraisal_format = models.ForeignKey('Appraisal_format', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, editable=False)
    deadline = models.DateField()

    class Meta:
        unique_together = ('presenter', 'topic', 'appraisal_format')

    def __str__(self):
        return f'{self.topic}'


class Appraisal(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, null=True, blank=True)
    attendee = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    criteria = models.ForeignKey('Criteria', on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('session', 'attendee', 'criteria')

    def __str__(self):
        return f'{self.id}'
