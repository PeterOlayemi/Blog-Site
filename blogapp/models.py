from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

AGE=(
    (0, 'Select Your Age Range'),
    (1, '0-12 years'),
    (2, '13-19 years'),
    (3, '20 years and above'),
    )

STATE = (
    (0, 'Select State'),
    (1, 'Abia'),
    (2, 'Adamawa'),
    (3, 'Akwa Ibom'),
    (4, 'Anambra'),
    (5, 'Bauchi'),
    (6, 'Bayelsa'),
    (7, 'Benue'),
    (8, 'Borno'),
    (9, 'Cross River'),
    (10, 'Delta'),
    (11, 'Ebonyi'),
    (12, 'Edo'),
    (13, 'Ekiti'),
    (14, 'Enugu'),
    (15, 'Gombe'),
    (16, 'Imo'),
    (17, 'Jigawa'),
    (18, 'Kaduna'),
    (19, 'Kano'),
    (20, 'Katsina'),
    (21, 'Kebbi'),
    (22, 'Kogi'),
    (23, 'Kwara'),
    (24, 'Lagos'),
    (25, 'Nasarawa'),
    (26, 'Niger'),
    (27, 'Ogun'),
    (28, 'Ondo'),
    (29, 'Osun'),
    (30, 'Oyo'),
    (31, 'Plateau'),
    (32, 'Rivers'),
    (33, 'Sokoto'),
    (34, 'Taraba'),
    (35, 'Yobe'),
    (36, 'Zamfara'),
    (37, 'FCT'),
)

class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin= models.BooleanField(default=False)
    is_writer = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    age = models.IntegerField(choices=AGE, default=0)
    state = models.IntegerField(choices=STATE, default=0)
    home_address = models.CharField(max_length=254)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class BlogModel(models.Model):
    blog_title = models.CharField(max_length=200, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    blog = models.TextField()
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"Blog: {self.blog_title}"
 
class CommentModel(models.Model):
    comment_text = models.TextField()
    blog = models.ForeignKey('BlogModel', on_delete=models.CASCADE)
    owned=models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"Comment by Name: {self.owned}"