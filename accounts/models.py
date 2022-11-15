from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
import random
import string


# def base64_to_image(base64_string):
#     format, imgstr = base64_string.split(';base64,')
#     ext = format.split('/')[-1]
#     return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)

class UserManager(BaseUserManager):
    def create_user(self,mobile, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not mobile:
            raise ValueError('Users must have an email address')
        if email:
            email=self.normalize_email(email)

        user = self.model(
            mobile=mobile,
            email=email,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, email=''):
        """
        Creates and saves a superuser with the given email and password.
        """

        user = self.create_user(mobile,
            email,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    class Meta:
        verbose_name = "User"  # set table records name
        verbose_name_plural = "Users"  # set table name

    mobile = models.CharField(max_length=12, unique=True,)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    gender = models.CharField(choices=(('1', 'Male'), ('2', 'Female'), ('0', 'NOT Set')), default='0',max_length=20)
    birth_date = models.DateField(blank=True, null=True)
    wallet_balance = models.CharField(max_length=10)
    profession = models.CharField(max_length=20)
    adhar_number = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True)
    advocate_license = models.ImageField(uploadher_to='advocate_license',blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    def name(self):
        return str(self.first_name) + ' ' + str(self.last_name)
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        return self.is_admin


class DeletedUser(models.Model):
    class Meta:
        verbose_name = "DeletedUser"  # set table records name
        verbose_name_plural = "DeletedUsers"  # set table name

    mobile = models.CharField(max_length=12, unique=True,)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,

    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    gender = models.CharField(choices=(('1', 'Male'), ('2', 'Female'), ('0', 'NOT Set')), default='0',max_length=20)
    birth_date = models.DateField(blank=True, null=True)
    wallet_balance = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    def name(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    @property
    def is_staff(self):
        return self.is_admin

class Otp(models.Model):
    credentials = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

#
# class ConnectRequest(models.Model):
#     from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
#     accept = models.CharField(choices=(('1', 'Accept'), ('0', 'Pending'), ('-1', 'Cancel'), ('-2', 'Delete')),
#                               max_length=20, default='0')
#
#     def user(self):
#         o = self.from_user
#         d = {'id': o.id, 'first_name': o.first_name, 'last_name': o.last_name,
#              'profile_image': str(o.profile_image), 'have_skills': o.have_skills}
#         return d
#
#     class Meta:
#         ordering = ['-id']
#
#
# class Profile_link(models.Model):
#     code = models.CharField(max_length=10, blank=True, null=False)
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#
#     def save(self, *args, **kwargs):
#         obj = Profile_link.objects.all().values('code')
#         print(kwargs, args)
#         S = 10
#         while True:
#
#             code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
#             if code in obj:
#                 pass
#             else:
#                 break
#         self.code = code
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.code
