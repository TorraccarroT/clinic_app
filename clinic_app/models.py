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
    doctor_id = models.CharField(max_length=100,blank=True)
    is_active = models.BooleanField(default=False)
    is_status = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    


from PIL import Image


class Data(models.Model):
    number = models.CharField(max_length=100)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    tel = models.CharField(max_length=100)
    sex = models.CharField(max_length=150)
    date = models.DateField(blank=True,null=True)
    drug_allergy = models.CharField(max_length=150)
    id_person  = models.CharField(max_length=150)
    career = models.CharField(max_length=150)
    address_current = models.CharField(max_length=150)
    name_company = models.CharField(max_length=150)
    tel_emergency = models.CharField(max_length=150)
    note = models.CharField(max_length=150)
    sickdisease = models.CharField(max_length=150)
    image_sick = models.ImageField(blank=True,upload_to='image')
    sick_status =  models.CharField(max_length=150,default=0)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.image_sick:
    #         img = Image.open(self.image_sick.path)
    #         if img.height >= 400 or img.width >= 400:
    #             output_size = (400, 400)
    #             img.thumbnail(output_size)
    #             img.save(self.image_sick.path)
class Save_Data(models.Model):
    person_data = models.ForeignKey(Data,on_delete=models.CASCADE)
    type_sick_data = models.CharField(max_length=150)
    sick_data = models.CharField(max_length=150)

class Shop_Product(models.Model):
    shop_code = models.CharField(max_length=100) 
    shop_name = models.CharField(max_length=100) 
    shop_qty = models.IntegerField() 
    shop_ps = models.CharField(max_length=100) 
    shop_type = models.CharField(max_length=100) 
    shop_count = models.CharField(max_length=100) 
    shop_price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    number = models.CharField(max_length=100)
    patient = models.ForeignKey(Data, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    credit_card = models.CharField(max_length=100)
    pay_check = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    pay_status = models.IntegerField(default=0)
    input_1 =  models.CharField(max_length=100,blank=True)
    input_2 =  models.CharField(max_length=100,blank=True)
    input_3 =  models.CharField(max_length=100,blank=True)
    doctor_1 = models.CharField(max_length=100,blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE)
    qty = models.IntegerField() 
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    sum_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    user_doctor = models.CharField(max_length=100,blank=True)


class OrderReport(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    order_number = models.CharField(max_length=100)
    created_at = models.DateField()
    credit_card = models.CharField(max_length=100)
    payment_date = models.DateField()
    item_name = models.CharField(max_length=100)
    item_count = models.CharField(max_length=100)
    item_quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_doctor = models.CharField(max_length=100,blank=True)

