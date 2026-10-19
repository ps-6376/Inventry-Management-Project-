from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class manager(models.Model):
    username=models.CharField(unique=True, max_length=30, default="username")
    Email=models.EmailField(unique=True)
    role=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    cnf_password=models.CharField()
    def set_password(raw_password):
        return make_password(raw_password)
    def check_password(self,raw_password):
        return check_password(raw_password,self.password)
    def __str__(self):
        return self.Email
    
# class consumer(models.Model):
#     username=models.CharField(unique=True, max_length=30, default="username")
#     Email=models.EmailField(unique=True)
#     password=models.CharField(max_length=20)
#     cnf_password=models.CharField()
#     def set_password(raw_password):
#             return make_password(raw_password)
#     def check_password(self,raw_password):
#             return check_password(raw_password,self.password)
#     def __str__(self):
#             return self.Email
class product_data(models.Model):
      product_id=models.CharField(unique=True)
      product_name=models.CharField(max_length=50)  
      category=models.CharField(max_length=30)
      supplier=models.CharField(max_length=50)
      description=models.CharField(max_length=300)
      image=models.ImageField(upload_to="product/")
      qunatity=models.IntegerField()
      unit=models.CharField(max_length=30)
      price_per_unit=models.FloatField()
      wherehouse_location=models.CharField(max_length=30)
      intial_status=models.CharField(max_length=30)
class deleted_data(models.Model):
       product_id=models.CharField(unique=True)
       product_name=models.CharField(max_length=50)  
       category=models.CharField(max_length=30)
       supplier=models.CharField(max_length=50)
       description=models.CharField(max_length=300)
       image=models.ImageField(upload_to="product/")
       qunatity=models.IntegerField()
       unit=models.CharField(max_length=30)
       price_per_unit=models.FloatField()
       wherehouse_location=models.CharField(max_length=30)
       intial_status=models.CharField(max_length=30)


      
      

      




    





    
    
    

# Create your models here.
