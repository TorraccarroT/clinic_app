from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin , AbstractUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=False, is_status=False):
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(username=username, is_active=is_active, is_status=is_status)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, is_active=True, is_status=True):
        return self.create_user(username, password, is_active, is_status)

class clinic_user(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=128)
    first_name =   models.CharField(max_length=128)
    last_name =  models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_status = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    


from PIL import Image


class Data(models.Model):
    number = models.CharField(max_length=10)
    firstname = models.CharField(max_length=15)
    lastname = models.CharField(max_length=15)
    tel = models.IntegerField()
    sex = models.CharField(max_length=15)
    date = models.DateField(blank=True,null=True)
    drug_allergy = models.CharField(max_length=15)
    id_person  = models.CharField(max_length=15)
    career = models.CharField(max_length=15)
    address_current = models.CharField(max_length=15)
    name_company = models.CharField(max_length=15)
    tel_emergency = models.CharField(max_length=15)
    note = models.CharField(max_length=15)
    sickdisease = models.CharField(max_length=15)
    image_sick = models.ImageField(blank=True,upload_to='image')
    sick_status =  models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image_sick:
            img = Image.open(self.image_sick.path)
            if img.height >= 400 or img.width >= 400:
                output_size = (100, 100)
                img.thumbnail(output_size)
                img.save(self.image_sick.path)
class Save_Data(models.Model):
    person_data = models.ForeignKey(Data,on_delete=models.CASCADE)
    type_sick_data = models.CharField(max_length=15)
    sick_data = models.CharField(max_length=15)

class Shop_Product(models.Model):
    shop_code = models.CharField(max_length=10) 
    shop_name = models.CharField(max_length=10) 
    shop_qty = models.IntegerField() 
    shop_ps = models.CharField(max_length=10) 
    shop_type = models.CharField(max_length=10) 
    shop_count = models.CharField(max_length=10) 
    shop_price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    number = models.CharField(max_length=10)
    patient = models.ForeignKey(Data, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    credit_card = models.CharField(max_length=10)
    pay_check = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    pay_status = models.IntegerField(default=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE)
    qty = models.IntegerField() 
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    sum_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
