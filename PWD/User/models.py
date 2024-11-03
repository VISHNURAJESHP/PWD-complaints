from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("User must have an email")

        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        print("PASSWORD IS", password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **vendor):
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


#Note: The administration wing is the head of all other wings so they are responsible for handling the whole wings
class official(AbstractBaseUser):

    WING = [
        ('national_highway','National_Highway'),
        ('road','Road'),
        ('buildings','Buildings'),
        ('bridges','Bridges'),
    ]
    id = models.BigAutoField(primary_key=True)
    #Profile_picture = models.ImageField(upload_to="vendor/profile", blank=True, null=True)
    employee_id = models.DecimalField(max_digits=10, decimal_places=10, null=True, unique=True)
    username = models.CharField(max_length=50)
    wing = models.CharField(max_length=255, choices= WING, null=True)
    designation = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=254,unique=True)
    head_of_wing = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def __str__(self):
        return self.username
    
    
class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=50)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(blank=False,null=True)
    created_date = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
    def is_otp_expired(self):
        if self.otp_created_at:
            expiration_time = self.otp_created_at + timedelta(minutes=5)
            return timezone.now() > expiration_time
        return True
