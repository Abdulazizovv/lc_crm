from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone_number, password, **extra_fields)
    
    def save(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class LearningCenter(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        pass


    def __str__(self) -> str:
        return self.title
    

class TeachGroup(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    learning_center = models.OneToOneField(LearningCenter, related_name='admin', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    

class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    fathers_name = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField()
    # image = models.ImageField(upload_to='student/images')
    learning_center = models.ManyToManyField(LearningCenter, related_name='students')
    groups = models.ManyToManyField(TeachGroup, related_name='students')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return str(self.first_name + ' ' + self.last_name)
    
    def __str__(self) -> str:
        return self.full_name


class TeacherProfile(models.Model):
    user = models.ForeignKey(User, related_name='teacher', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    learning_center = models.ManyToManyField(LearningCenter, related_name='teachers')
    groups = models.ManyToManyField(TeachGroup, related_name='teachers')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @property
    def full_name(self):
        return str(self.first_name + ' ' + self.last_name)
    
    def __str__(self) -> str:
        return self.full_name
    