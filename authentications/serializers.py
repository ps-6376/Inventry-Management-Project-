
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import product_data,deleted_data,userProfile

class signupserializers(serializers.ModelSerializer):
    password=serializers.CharField(max_length=30)
    cnf_password=serializers.CharField(max_length=30)
    class Meta:
        model=User
        fields=[
            "username",
            "email",
            "password",
            "cnf_password"
        ]
    def validate(self, data):
        if data["password"]!=data["cnf_password"]:
            raise serializers.ValidationError({
                "cnf_password":"password do not match"
            })
        return data
    def create(self, validated_data):
          validated_data.pop("cnf_password")
        
          new_user=User.objects.create_user(
             username=validated_data["username"],
             email=validated_data["email"],
             password=validated_data["password"]
             )
          userProfile.objects.create(
                user=new_user,
                role="consumer"
           )
          print("user created")
          return new_user
class add_productserializers(serializers.ModelSerializer):
    print("inside add product serializer")
    class Meta:
            model=product_data
            fields=[
                "product_id",
                "product_name",
                "category",
                "supplier",
                "description",
                "image",
                "qunatity",
                "unit",
                "price_per_unit",
                "wherehouse_location",
                "intial_status"
            ]       
# class delete_productserializer(serializers.ModelSerializer):
#      print("inside delete product serializer")
#      class Meta:
#             model=deleted_data
#             fields=[
#                 "product_id",
#                 "product_name",
#                 "category",
#                 "supplier",
#                 "description",
#                 "image",
#                 "qunatity",
#                 "unit",
#                 "price_per_unit",
#                 "wherehouse_location",
#                 "intial_status"
#             ]       

   # def create(self, data):
    #     print("inside create function")
    #     new_product=product_data.objects.create(
    #           product_id=data["product_id"],
    #           product_name=data["product_name"],
    #           category=data["category"],
    #           supplier=data["supplier"],
    #           description=data["description"],
    #           image=data["image"],
    #           qunatity=data["qunatity"],
    #           unit=data["unit"],
    #           price_per_unit=data["price_per_unit"],
    #           wherehouse_location=data["wherehouse_location"],
    #           intial_status=data["intial_status"]
    #         )
        # print("new product is created")
        # return new_product






        






        