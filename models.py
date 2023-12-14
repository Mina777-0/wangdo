from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, password= None, **extra_fields):
        if not email:
            raise ValueError("email address must be provided")
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password= None, **extra_fields):
        user = self.create_user(email, password=password)
        user.admin= True
        user.save()
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, verbose_name="email address", unique= True)
    

    is_staff= models.BooleanField(default= False)
    is_active= models.BooleanField(default= True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects= MyUserManager()

    def __str__(self):
        return self.email
    

class Product(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()
    image = models.ImageField(null=False, blank=False, upload_to="media/")
    price = models.FloatField()
    slug = models.SlugField()

    def __str__(self):
        return self.title
