from django.db import models
from passlib.hash import pbkdf2_sha256
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
from passlib.hash import pbkdf2_sha256
from django.core.validators import MinLengthValidator, MaxLengthValidator
from datetime import datetime
from django.core.exceptions import ValidationError

from pytz import timezone 
IST = 'Asia/Kolkata'
def validate_phone(value):
    if type(value) != str:
        raise ValidationError(
            ('%(value)s is not a string'),
            params={'value': value},
        )
    for x in value:
        try:
            int(x)
        except:
            raise ValidationError(
            ('%(value)s is not a number'),
            params={'value': value},
            )
    if len(value) != 10:
            raise ValidationError(
            ('Length of phone number is not equal to 10')

            )
class UserProfile(User):
    user_id = models.CharField(unique=True,db_index=True,max_length = 10)
    contact_number = models.CharField(validators = [MaxLengthValidator(10),MinLengthValidator(10)],unique= True,max_length = 10)
    name = models.CharField(max_length = 200)

    #email_id = models.CharField(max_length=200, default = "email_obsolete@obs.com")
    #username = models.CharField(max_length = 200,unique=True)

    # User Type will be useful for permissions in the future
    user_type = models.IntegerField(default = 3,null=False)

    #def __str__(self):
    #    return self.email_id
class Category(models.Model):
    category_id = models.CharField(max_length = 10, db_index = True, unique = True)
    category_name = models.CharField(max_length = 20, unique = True, db_index = True)
    category_image_name = models.CharField(max_length = 50)
    def __str__(self):
        return self.category_id + ' ' + self.category_name
class Services(models.Model):
    service_id = models.CharField(max_length = 10, db_index = True,  unique=True)
    service_name = models.CharField(max_length = 300, db_index=True)
    #category_name_shortened = models.CharField(max_length = 100)
    service_description = models.CharField(max_length = 500)
    service_image_name = models.CharField(max_length = 100)
    #service_locations = ListCharField(
    #    models.CharField(max_length = 100),
    #    default=list,
    #    null=False,
    #    max_length = 99999
    #)

    service_providers = ListCharField(
        models.CharField(max_length = 100),
        default=list,
        null=False,
        max_length = 99999
    )
    category = models.CharField(max_length = 10)
    service_visible = models.BooleanField(default = False)
    def __str__(self):
        return self.service_name

class Orders(models.Model):
    order_id = models.CharField(max_length = 10, unique  = True, db_index = True)
    order_customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order_services = ListCharField(
        models.CharField(max_length = 300),
        default=list,
        null=False,
        max_length = 99999
    )
    order_total_bill  = models.FloatField(default = 0)

    def __str__(self):
        return self.order_id

class Locations(models.Model):
    location_id = models.CharField(max_length = 10, db_index = True, unique = True)
    location_name = models.CharField(max_length = 150, db_index = True)

    def __str__(self):
        return self.location_name


class ServiceProviders(models.Model):
    provider_id = models.CharField(max_length = 10, unique = True, db_index = True)
    provider_name = models.CharField(max_length = 300, db_index=True)
    provider_number = models.CharField(max_length = 10, validators=[validate_phone])
    provider_location = models.ForeignKey(Locations, on_delete = models.CASCADE)
    provider_image_name = models.CharField(max_length = 100, default = 'default.jpg')
    provider_service = models.ForeignKey(Services, on_delete = models.CASCADE)
    provider_bio = models.CharField(max_length = 500, default = "No Bio")
    def __str__(self):
        return self.provider_id + '  ' + self.provider_name
    
class Dummy(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length = 150)
    
    location = models.CharField(max_length =100)
    message = models.CharField(max_length = 200)
    def __str__(self):
        return self.name + ' ' + self.email

class PasswordReset(models.Model):
    email = models.CharField(max_length = 150, unique = True)
    otp_id = models.CharField(max_length = 50, unique = True)
    def __str__(self):
        return self.email + ' '+ self.otp_id
