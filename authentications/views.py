from django.shortcuts import render,redirect
from rest_framework import status

from rest_framework.response import Response
# from .models import user_cred
from rest_framework.views import APIView
from .serializers import Userserializers,consumerserializers,add_productserializers
from rest_framework import status
from .models import product_data,deleted_data, manager
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.urls import reverse

class UserSignupApiView(APIView):
     def get(self, request):
                print("get the request")
                return render(request,'signup_user.html')
     def post(self,request):
            print("inside post")
            serializer = Userserializers(data=request.data)
            if serializer.is_valid():
                 print("user arguments are valid")
                 user = serializer.save()   
                 pageurl=reverse("login")
                 return Response(
                       {"message":"Manager is seccefully signup",
                        "username":user.username,
                        "email":user.Email,
                        "pageurl":pageurl
                        },
                        status=status.HTTP_201_CREATED
                 )
            print("not validate user")
            print(serializer.errors)
            return Response(
              serializer.errors,
              status=status.HTTP_400_BAD_REQUEST      
        )
class ConsumerSignupApiView(APIView):
     def get(self, request):  
           print("get request from consumer")
           return render(request,'signup_consumer.html')
     def post(self,request):
            print("inside consumer post")
            serializer =consumerserializers(data=request.data)
            if serializer.is_valid():
                 print("consumer arguments are valid")
                 consumer = serializer.save()    
                 pageurl=reverse("login")
                 return Response(
                       {
                         "msg":"user is sucessfully registred",
                         "username": consumer.username,
                         "Email": consumer.email,
                         "pageurl": pageurl

                       }, status=status.HTTP_201_CREATED
                 )
            return Response(
                  serializer.errors,
                  status=status.HTTP_400_BAD_REQUEST
            )
class LoginAPIView(APIView):
        def get(self, request):
            print("get request in loginview")
            return render(request,'login.html')
        def post(self, request):
               print("inside post login")
               email = request.data.get("Email")
               password = request.data.get("password")
               role=request.data.get("role")
               if role=="user":
                     try:
                           user_obj= manager.objects.get(Email=email)

                     except user_obj.DoesNotExist:
                             return Response(
                                   {
                                    "error":"Email entered is Not Correct"
                                   },
                                   status=status.HTTP_401_UNAUTHORIZED
                             )
                     if user_obj.check_password(password):
                           if user_obj.role=="manager":
                               username=user_obj.username
                               request.session["username"] = username
                               page_url=reverse("manager")
                               return Response(
                                     {"message":"Manager is login Seccefully",
                                      "username":username,
                                      "pageurl":page_url
                                      },
                                     status=status.HTTP_200_OK
                               )
                           else:
                                return redirect("supervisor")

                     else:
                         return Response({
                               "error":"Password is not correct",
                         },
                         status=status.HTTP_401_UNAUTHORIZED
                         )
               else:
                     print("inside consumer condition")
                     user=authenticate(request,
                                  email=email,
                                  password= password)
                     print(user)
                     if user is None:
                           return Response(
                                 {"error": "Email and password are not correct"},
                                 status=status.HTTP_401_UNAUTHORIZED

                           )
                     token,created=Token.objects.get_or_create(
                           user=user
                     )
                     page_url=reverse("consumer")
                     return Response({
                           "message":"consumer is succefully login",
                           "token":token.key,
                           "username":user.username,
                           "pageurl": page_url
                     },
                     status=status.HTTP_200_OK)


                           
                           
                  #   try:
                  #       user_obj=consumer.objects.get(Email=Email)
    
                  #   except consumer.DoesNotExist:
                  #           msg="Email is not registerd"
                  #           return render(request,"signup_consumer.html",msg)
                  #   if user_obj.check_password(password):
                  #       return redirect("consumer")
    
                  #   else:
                  #        msg="password is not correct"
                  #        return render(request,"signup_consumer.html",msg)
    
class managerAPIView(APIView):
      def get(self, request): 
         username=request.query_params.get("username")
         rows= product_data.objects.count()
         Available_item=product_data.objects.all().filter(intial_status="Available").count()
         low_stock_item=product_data.objects.all().filter(intial_status="Low Stock").count()
         out_of_stock=product_data.objects.all().filter(intial_status="out of stock").count()
         per_avai_stock=rows*Available_item/100
         No_of_units=product_data.objects.values("unit").distinct().count()
         most_repeated_loc=product_data.objects.values("wherehouse_location").distinct().count()
         max_qunatity = product_data.objects.order_by(
            'qunatity'
        ).first()
         most_quantity_product=max_qunatity.product_name
         max_price = product_data.objects.order_by(
                     'price_per_unit'
                 ).first()
         max_price_per_unit_product= max_price.product_name

         return render(request,"manager.html",{"username":username,"rows":rows,"Available_item":Available_item,"low_stock_item": low_stock_item,"out_of_stock":out_of_stock,"per_avai_stock":per_avai_stock,"No_of_units":No_of_units,"most_repeated_loc":most_repeated_loc,"most_quantity_product":most_quantity_product,"max_price_per_unit_product":max_price_per_unit_product})    
class ConsumerAPIView(APIView):
      def get(self, request): 
               return render(request,"consumer.html")
        
class add_inventryAPIView(APIView):
      parser_classes = [MultiPartParser, FormParser]
      def get(self, request):
            username = request.session.get("username")
            print("add product get request")
            return render(request,"add_inventry.html",{"username":username})
      def post(self, request):
        print("inside post")
        print(request.data)
        serializer=add_productserializers(data=request.data)
        print("serializer created")
        if serializer.is_valid():
            product_data=serializer.save()              
            print("product is valid") 
            pageurl=reverse("add_inventry")
            return Response(
                  {"Sucess":"The product added sucessfully",
                   "pageurl":pageurl
                   },status=status.HTTP_201_CREATED
            ) 
        else:
              return Response(
                    {
                          "message":"add product argument is not valid",
                          "error":serializer.errors
                    },status=status.HTTP_400_BAD_REQUEST
              )
class view_inventryAPIView(APIView):
      def get(self,request):
            print("inside get of view")
            username = request.session.get("username")
            products=product_data.objects.all()
            return render(request,"view_inventry.html",{"products":products,"username":username})
      def post(self, request):
           print("inside post of view")
           filter_category =request.data.get("filter_category")
           filter_status= request.data.get("filter_status")
           print(filter_category)
           print(filter_status)
           if filter_category!=None and filter_status!=None:
                  print("inside filter request")
                  if filter_category=="All categories" and filter_status=="All statuses":
                        products=product_data.objects.all()
                        return render(request,"view_inventry.html",{"products":products})
                  elif filter_category!="All categories" and filter_status=="All statuses":
                        products=product_data.objects.all().filter(category=filter_category)
                        return render(request,"view_inventry.html",{"products":products})
                  elif filter_status!="All statuses" and filter_category=="All categories":
                              products=product_data.objects.all().filter(intial_status=filter_status)   
                              return render(request,"view_inventry.html",{"products":products})   
                  else:
                        products=product_data.objects.all().filter(category=filter_category,intial_status=filter_status)
                        return render(request,"view_inventry.html",{"products":products})
           else:
                 print("inside delete request")
                 id=request.data.get("product_id")
                 print(id)
                 row=product_data.objects.get(product_id=id)
                 product_id=row.product_id
                 product_name=row.product_name
                 category=row.category
                 supplier=row.supplier
                 description=row.description
                 image=row.image
                 qunatity=row.qunatity
                 unit=row.unit
                 price_per_unit=row.price_per_unit
                 wherehouse_location=row.wherehouse_location
                 intial_status=row.intial_status
                 deleted_data.objects.create(
                       product_id=product_id,
                       product_name=product_name,
                       category=category,
                       supplier=supplier,
                       description=description,
                       image=image,
                       qunatity=qunatity,
                       unit=unit,
                       price_per_unit=price_per_unit,
                       wherehouse_location=wherehouse_location,
                       intial_status=intial_status
                 )
                 print("data in saved in delete dDS")
            #      serializer=delete_productserializer(data=row)
            #      print("serializer is created for delete")
            #      if serializer.is_valid():
            #            serializer.save()
            #            print("row created in delete database")
            #      else:  
            #            return Response(
            #                  {
            #                  "Erroe_message":"Argument passesd In Delete Serializer is Not valid  ",
            #                  "error":serializer.errors
            #                  }
            #            )
                 row.delete()
                 print("row is deleted")
                 products=product_data.objects.all()
                 return render(request,"view_inventry.html",{"products":products})               
class update_inventryAPIView(APIView):
      def get(self, request):
         print("inside get of update")
         username = request.session.get("username")
         return render(request,"update_inventry.html",{"username":username})
      def post(self,request):
            print("inside the post of update")
            btn_val=request.data.get("action")
            if btn_val=="cancel":
                  return redirect("update_inventry")
            if btn_val=="load":
                  product_id=request.data.get("product_id")or None
                  if product_id:   
                      print("inside the load")
                      row=product_data.objects.get(product_id=product_id)
                      return render(request,"update_inventry.html",{"row":row})
                  else:
                        error_msg="Pleaes Enter Product ID to load Data"
                        return render(request,"update_inventry.html",{"error_msg":error_msg})  

            elif btn_val=="save":
                  print("inside the save")
                  product_id=request.data.get("product_id")or None
                  product_name=request.data.get("product_name")or None
                  category=request.data.get("category")or None
                  supplier=request.data.get("supplier")or None
                  description=request.data.get("description")or None
                  unit=request.data.get("unit")or None
                  qunatity=request.data.get("qunatity")or None
                  price_per_unit=request.data.get("price_per_unit")or None
                  image=request.data.get("image")or None
                  wherehouse_location=request.data.get("wherehouse_location")or None
                  intial_status=request.data.get("intial_status")or None
                  print(product_id)
                  print(supplier)
                  print(description)
                  print("changed feilds data in collected")
                  update_data={}

                  if product_name:
                        print("inside product name condition")
                        update_data["product_name"]=product_name
                        # product_data.objects.filter(product_id=product_id).update(product_name=product_name)
                  if category!="select":
                        print("inside category condition")
                        update_data["category"]=category
                        # product_data.objects.filter(product_id=product_id).update(category=category)
                  if supplier:
                        print("inside supplier condition")
                        update_data["supplier"]=supplier
                        # product_data.objects.filter(product_id=product_id).update(supplier=supplier)
                  if description:
                        print("inside description condition")
                        update_data["description"]=description
                        # product_data.objects.filter(product_id=product_id).update(description=description)
                  if unit!="select":
                        print("inside unit condition")
                        update_data["unit"]=unit
                        # product_data.objects.filter(product_id=product_id).update(unit=unit)
                  if qunatity:
                         print("inside unit condition")
                         update_data["qunatity"]=qunatity
                        # product_data.objects.filter(product_id=product_id).update(qunatity=qunatity)
                  if price_per_unit:
                        print("inside price_per_unit condition")
                        update_data["price_per_unit"]=price_per_unit
                        # product_data.objects.filter(product_id=product_id).update(price_per_unit=price_per_unit)
                  if image:
                        print("inside image condition")
                        update_data["image"]=image
                        # product_data.objects.filter(product_id=product_id).update(image=image)
                  if wherehouse_location:
                        print("inside wherehouse location condition")
                        update_data["wherehouse_location"]=wherehouse_location

                        # product_data.objects.filter(product_id=product_id).update(wherehouse_location=wherehouse_location)
                  if intial_status!="select":
                        print("inside intial_status condition")
                        update_data["intial_status"]=intial_status
                        # product_data.objects.filter(product_id=product_id).update(intial_status=intial_status)
                  if update_data:
                        product_data.objects.filter(
                              product_id=product_id
                        ).update(**update_data)
                        print("data in updated")
                        products=product_data.objects.all()
                        return render(request,"view_inventry.html",{"products":products})
                  else:
                        msg="No changes are made"
                        return render(request,"update_inventry.html",{"msg":msg})
       
class delete_inventryAPIView(APIView):
      def get(self, request):
            deleted_products=deleted_data.objects.all()
            username = request.session.get("username")
            print(deleted_products)
            return render(request,"delete_inventry.html",{"deleted_products":deleted_products,"username":username})
      def post(self, request):
            product_filter=request.data.get("product_filter")
            if product_filter:
                  deleted_products=deleted_data.objects.all().filter(product_id=product_filter)     
                  return render(request,"delete_inventry.html",{"deleted_products": deleted_products})
            checkbox_status=request.data.getlist("checkbox")
            action=request.data.get("action")
            print(checkbox_status)
            if action =="cancel":
                deleted_products=deleted_data.objects.all()
                return render(request,"delete_inventry.html",{"deleted_products":deleted_products})
            if checkbox_status:
               print("checkbox status is on")
               count=len(checkbox_status)
               print("this is the count of items =",count)
               for product_id in checkbox_status:
                      print(product_id)
                      row=deleted_data.objects.get(product_id=product_id)
                      if action=="restore":
                            product_data.objects.create(
                              product_id=row.product_id,
                              product_name=row.product_name,
                              category=row.category,
                              supplier=row.supplier,
                              description=row.description,
                              image=row.image,
                              qunatity=row.qunatity,
                              unit=row.unit,
                              price_per_unit=row.price_per_unit,
                              wherehouse_location=row.wherehouse_location,
                              intial_status=row.intial_status,
                          )

                            row.delete() 
                            
                      else:
                            row.delete()
               deleted_products=deleted_data.objects.all()
               return render(request,"delete_inventry.html",{"deleted_products":deleted_products,"count":count})
            else:
                  return Response({
                        "msg":"Please select the checkbox first"
                  })
            
                           
# consumer deshboard
class ConsumerAPIView(APIView):
       def get(self, request):
            print("get request in consumer desboard")
            username=request.query_params.get("username")
            total_product= product_data.objects.count()
            all_products= product_data.objects.all()
            return render(request,"consumer_dashboard.html",{"username":username,"total_product":total_product,"all_products":all_products})
       def post(self, request): 
            print("inside post of cosumer deshboard")
            print("Request data:", request.data)
            searchvalue=request.data.get("searchvalue")
            print(searchvalue)
            products=product_data.objects.all().filter(product_name=searchvalue)
            print(products)  
            if products:
                 print("products is available")
                 return Response({
                     "products":products
                  },
                  status=status.HTTP_200_OK
                  )
            else:
                print("products is not available")
                return Response({
                      "msg":"This product is not available"
                },
            #     status=status.HTTP_400_BAD_REQUEST
                )
class Add_CartAPIView(APIView):
       def get(self, request):
            print("get the request in addcart")
            product_id = request.query_params.get("product_id")
            print(product_id)
            if not product_id:
                  print("product id not have value")
                  return Response(
                      {"error": "Product ID is required"},
                      status=status.HTTP_400_BAD_REQUEST
                  )
                  # Retrieve the product from the database
            cart_product_ids = request.session.get(
                  "cart_product_ids", []
            )
            # Add the new product ID
            if product_id not in cart_product_ids:
                  cart_product_ids.append(product_id)

            # Save the updated list in the session
            request.session["cart_product_ids"] = cart_product_ids
            return Response({
                  "message": "Product added to cart successfully",
      
        }, status=status.HTTP_200_OK)
class cartpageAPIView(APIView):
      def get(self, request):
            print("get inside the cart page")
            cart_product_ids = request.session.get("cart_product_ids", [])
            cart_items=[]
            total_prices=[]
            for product_id in cart_product_ids:
                  if product_id:
                        try:
                              cart_item= product_data.objects.get( 
                                    product_id=product_id)
                              total_price =cart_item.price_per_unit*cart_item.qunatity
                              total_prices.append(total_price)
                              cart_items.append(cart_item)
                              print("fatched cart item")
                        except product_data.DoesNotExist:
                              product = None 
            len_of_cart=len(cart_items)
            len_of_totalprice=len(total_prices)
            return render(
                  request,
                  "cart.html",
                  { "cart_items":cart_items ,"total_prices":total_prices}
            )
class orderAPIView(APIView):
      def get(self, request):
            return render(request,"orders.html")
      
class profileAPIView(APIView):
      def get(self, request):
          return render(request,"profile.html")

            
        
      

     

#     if request.method=="POST":
#          Email=request.POST.get("email")
#          passw=request.POST.get("passw")
#          cnf_passw=request.POST.get("cnf_passw")
#          role=request.POST.get("role")
#          print(Email)
#          print(passw)
#          print(cnf_passw)
#          print(role)


   
# def login(request):
#     if request.method=="POST":
#          uname=request.POST.get("uname")
#          passw=request.POST.get("passw")
#          print(uname)
#          print(passw)
#          result=user_cred.objects.filter(
#              username=uname,
#              password=passw 
#          ).exists()
         

             
    
    # return render(request,'login.html')

# Create your views here.
