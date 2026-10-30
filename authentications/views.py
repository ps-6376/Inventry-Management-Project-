from django.shortcuts import render,redirect
from rest_framework import status

from rest_framework.response import Response 
from rest_framework.views import APIView
from .serializers import signupserializers,add_productserializers
from rest_framework import status
from .models import product_data,deleted_data, userProfile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.urls import reverse
# from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

class  SignupApiView(APIView):
     def get(self, request):  
           print("get request from consumer")
           return render(request,'signup.html')
     def post(self,request):
            print("inside signup post")
            serializer =signupserializers(data=request.data)
            if serializer.is_valid():
                 print("signup seriallzer arguments are valid")
                 user = serializer.save()    
                 pageurl=reverse("login")
                 return Response(
                       {
                         "msg":"user is sucessfully registred",
                         "username": user.username,
                         "Email": user.email,
                         "pageurl": pageurl

                       }, status=status.HTTP_201_CREATED
                 )
            return Response(
                  serializer.errors,
                  status=status.HTTP_400_BAD_REQUEST
            )
# class Adminapiview(APIView):
#     permission_classes = [IsAdminUser]
#     def get(self,request):
#           return render(request,"Admin.html")
#     def post(self,request):
#        email=request.data.get("email")
#        new_role = request.data.get("role")
#        if new_role not in ["consumer", "manager"]:
#             return Response(
#                 {"error": "Invalid role"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#        try:
#             user = User.objects.get(email__iexact=email)
#        except User.DoesNotExist:
#             return Response(
#                 {"error": "User not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         # Find the user's profile
#        try:
#             profile =  userProfile.objects.get(user=user)
#        except  userProfile.DoesNotExist:
#             return Response(
#                 {"error": "User profile not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#        profile.role = new_role
#        profile.save()
       
#        return Response({
#             "message": "User role updated successfully",
#             "email": user.email,
#             "role": profile.role
#         }, status=status.HTTP_200_OK)





class LoginAPIView(APIView):
        def get(self, request):
            print("get request in loginview")
            return render(request,'login.html')
        def post(self, request):
               print("inside post login")
               email = request.data.get("Email")
               password = request.data.get("password")
                    
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
               role = user.userprofile.role
               print(role)
               if role=="manager":
                     page_url=reverse("manager")
                     return Response({
                           "message":"Manager is succefully login",
                           "token":token.key,
                           "username":user.username,
                           "pageurl": page_url
                        },
                        status=status.HTTP_200_OK
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
         print("get method inside manager api view")
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
         return Response(
               {
                "rows":rows,
                "Available_item":Available_item,
                "low_stock_item": low_stock_item,
                "out_of_stock":out_of_stock,
                "per_avai_stock":per_avai_stock,
                "No_of_units":No_of_units,
                "most_repeated_loc":most_repeated_loc,
                "most_quantity_product":most_quantity_product,
                "max_price_per_unit_product":max_price_per_unit_product
                },
                 status=status.HTTP_200_OK
         )
def manager_page(request):
     print("inside manager page")
     return render(request, "manager.html")
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
              print("Serializer errors:", serializer.errors)
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
            data = []
            for product in products:
                  data.append({
                  "product_id": product.product_id,
                  "product_name": product.product_name,
                  "category": product.category,
                  "supplier": product.supplier,
                  "qunatity": product.qunatity,
                  "unit": product.unit,
                  "price_per_unit": product.price_per_unit,
                  "wherehouse_location": product.wherehouse_location,
                  "intial_status": product.intial_status,
                  })

            return Response({
                  "data":data,
                  "username":username
            },
             status=status.HTTP_200_OK 
            )
      def post(self, request):
           print("inside post of view")
           filter_category =request.data.get("filter_category")
           filter_status= request.data.get("filter_status")
           print(filter_category)
           print(filter_status)
           if filter_category!=None and filter_status!=None:
                  print("inside filter request")
                  if filter_category=="All categories" and filter_status=="All statuses":
                        print("inside all category and all status condition")
                        products=product_data.objects.all()
                        data = []

                        for product in products:
                              data.append({
                              "product_id": product.product_id,
                              "product_name": product.product_name,
                              "category": product.category,
                              "supplier": product.supplier,
                              "qunatity": product.qunatity,
                              "unit": product.unit,
                              "price_per_unit": product.price_per_unit,
                              "wherehouse_location": product.wherehouse_location,
                              "intial_status": product.intial_status,
                              })

                       
                              return Response({ 
                                    "data":data
                              },
                              status=status.HTTP_200_OK
                              )
                  elif filter_category!="All categories" and filter_status=="All statuses":
                        products=product_data.objects.all().filter(category=filter_category)
                        data = []
                        for product in products:
                              data.append({
                              "product_id": product.product_id,
                              "product_name": product.product_name,
                              "category": product.category,
                              "supplier": product.supplier,
                              "qunatity": product.qunatity,
                              "unit": product.unit,
                              "price_per_unit": product.price_per_unit,
                              "wherehouse_location": product.wherehouse_location,
                              "intial_status": product.intial_status,
                              })
                        
                        return Response({ 
                                          "data":data,
                                          },
                                          status=status.HTTP_200_OK
                        )
                  elif filter_status!="All statuses" and filter_category=="All categories":
                              products=product_data.objects.all().filter(intial_status=filter_status) 
                              data = []
                              for product in products:
                                    data.append({
                                    "product_id": product.product_id,
                                    "product_name": product.product_name,
                                    "category": product.category,
                                    "supplier": product.supplier,
                                    "qunatity": product.qunatity,
                                    "unit": product.unit,
                                    "price_per_unit": product.price_per_unit,
                                    "wherehouse_location": product.wherehouse_location,
                                    "intial_status": product.intial_status,
                                    })
                              
                              return Response({ 
                                                "data":data
                                                
                                                },status=status.HTTP_200_OK
                                          )  
                                
                  else:
                        products=product_data.objects.all().filter(category=filter_category,intial_status=filter_status)
                        data = []
                        
                        for product in products:
                              data.append({
                              "product_id": product.product_id,
                              "product_name": product.product_name,
                              "category": product.category,
                              "supplier": product.supplier,
                              "qunatity": product.qunatity,
                              "unit": product.unit,
                              "price_per_unit": product.price_per_unit,
                              "wherehouse_location": product.wherehouse_location,
                              "intial_status": product.intial_status,
                              })
                        
                        return Response({ 
                                    "data":data
                                    },status=status.HTTP_200_OK
                              )  
           else:
                 id=request.data.get("product_id")
                 if id: 
                        print("inside delete condition")
                        print(id)
                        row=product_data.objects.get(product_id=id)
                        deleted_data.objects.create(
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
                              intial_status=row.intial_status
                        )
                        print("data in saved in delete dDS")
                        row.delete()
                        print("row is deleted")
                        products=product_data.objects.all()
                        data = []

                        for product in products:
                                    data.append({
                                    "product_id": product.product_id,
                                    "product_name": product.product_name,
                                    "category": product.category,
                                    "supplier": product.supplier,
                                    "qunatity": product.qunatity,
                                    "unit": product.unit,
                                    "price_per_unit": product.price_per_unit,
                                    "wherehouse_location": product.wherehouse_location,
                                    "intial_status": product.intial_status,
                                    })
                        
                        return Response(
                              {"data":data},
                              status=status.HTTP_200_OK
                        )    
                 else:
                     return Response(
                           {"msg":"product id not receiced for delete"},
                           status=status.HTTP_400_BAD_REQUEST
                     )
                                                
                       
def view_inventry(request):
     print("inside view page")
     return render(request, "view_inventry.html")
class update_inventryAPIView(APIView):
      def get(self, request):
         print("inside get of update")
         username = request.session.get("username")
         return Response(
               {
                "username":username
                },
                status=status.HTTP_200_OK
            )
      def post(self,request):
            print("inside the post of update")
            data=[]
            load_item=request.data.get("load_item")
            savebtn=request.data.get("savebtn")
            if load_item:
                  product_id=request.data.get("product_id")or None
                  if product_id:   
                      print("inside the load")
                      product=product_data.objects.get(product_id=product_id)
                      load_data={
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "category": product.category,
                        "supplier": product.supplier,
                        "qunatity": product.qunatity,
                        "unit": product.unit,
                        "price_per_unit": product.price_per_unit,
                        "wherehouse_location": product.wherehouse_location,
                        "intial_status": product.intial_status,
                        }

                      return Response(
                            {"load_data":load_data
                             }, status=status.HTTP_200_OK
                      )
                  else:
                        error_msg="Pleaes Enter Product ID to load Data"
                        return Response(
                                    {"error_msg":error_msg
                                     },
                                    status=status.HTTP_400_BAD_REQUEST    
                              )

            elif savebtn:
                  print("inside form data")
                  product_id = request.data.get("product_id")

                  if not product_id:
                        return Response(
                        {"error": "Product ID is required"},
                        status=status.HTTP_400_BAD_REQUEST
                        )

                  # Step 2: Fetch the specific product row
                  try:
                        product = product_data.objects.get(
                        product_id=product_id
                        )
                  except product_data.DoesNotExist:
                        return Response(
                        {"error": "Product not found"},
                        status=status.HTTP_404_NOT_FOUND
                        )

                  # Step 3: Allow only the fields that can be updated
                  allowed_fields = [
                  "product_name",
                  "category",
                  "supplier",
                  "description",
                  "unit",
                  "qunatity",
                  "price_per_unit",
                  "wherehouse_location",
                  "intial_status",
                  "image"
                  ]

                  updated_fields = []

                  for field in allowed_fields:

                  # Update only fields received from JavaScript
                        if field in request.data:

                              value = request.data[field]

                              setattr(product, field, value)

                              updated_fields.append(field)

                        # Save changes to the database
                        if updated_fields:
                           product_data.save(update_fields=updated_fields)

            return Response(
            {
                  "message": "Product updated successfully"
            },
            status=status.HTTP_200_OK
                        )

                  
               
def update_inventry(request):
     print("inside view page")
     return render(request, "update_inventry.html")  

class delete_inventryAPIView(APIView):
      def get(self, request):
            delete_data=[]
            del_products=deleted_data.objects.all()
            username = request.session.get("username")
            for product in del_products:
               delete_data.append({
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "category": product.category,
                        "supplier": product.supplier,
                        "qunatity": product.qunatity,
                        "unit": product.unit,
                        "price_per_unit": product.price_per_unit,
                        "wherehouse_location": product.wherehouse_location,
                        "intial_status": product.intial_status,
                  }
                  )
            return Response(
                  {
                  "delete_data":delete_data,
                  "username":username
                  },
                    status=status.HTTP_200_OK

                  )
      def post(self, request):
            print("inside post request")
            product_filter=request.data.get("product_filter")
            delete_data=[]
            if product_filter:
                  print("get filter id condition")
                  del_products=deleted_data.objects.all().filter(product_id=product_filter)  
                  for product in del_products:
                        delete_data.append({
                              "product_id": product.product_id,
                              "product_name": product.product_name,
                              "category": product.category,
                              "supplier": product.supplier,
                              "qunatity": product.qunatity,
                              "unit": product.unit,
                              "price_per_unit": product.price_per_unit,
                              "wherehouse_location": product.wherehouse_location,
                              "intial_status": product.intial_status,
                        }
                        )
                  return Response(
                        {"delete_data": delete_data
                         },
                        status=status.HTTP_200_OK
                  )   
           
            deletebtn=request.data.get("deletebtn")
            restorebtn=request.data.get("restorebtn")
            product_ids =request.data.get("product_ids")
            
            print(product_ids )
            if product_ids :
               print("products ids geted")
               count=len(product_ids)
               print("this is the count of items =",count)
               for product_id in product_ids :
                      print(product_id)
                      row=deleted_data.objects.get(product_id=product_id)
                      if restorebtn:
                            print("inside the restore condition")
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

                            del_products=deleted_data.objects.all()
                            
                            for product in del_products:
                                    delete_data.append({
                                          "product_id": product.product_id,
                                          "product_name": product.product_name,
                                          "category": product.category,
                                          "supplier": product.supplier,
                                          "qunatity": product.qunatity,
                                          "unit": product.unit,
                                          "price_per_unit": product.price_per_unit,
                                          "wherehouse_location": product.wherehouse_location,
                                          "intial_status": product.intial_status,
                                    })

                               
                            return Response({
                                    "delete_data":delete_data,
                                    }, status=status.HTTP_200_OK
                                    )
                         
                      elif deletebtn:
                              print("inside delete item condition")
                              row.delete()
                              del_products=deleted_data.objects.all()
                              for product in del_products:
                                    delete_data.append({
                                          "product_id": product.product_id,
                                          "product_name": product.product_name,
                                          "category": product.category,
                                          "supplier": product.supplier,
                                          "qunatity": product.qunatity,
                                          "unit": product.unit,
                                          "price_per_unit": product.price_per_unit,
                                          "wherehouse_location": product.wherehouse_location,
                                          "intial_status": product.intial_status,
                                    })
                              
                              return Response({
                                    "delete_data":delete_data,
                                    "count":count
                                    }, status=status.HTTP_200_OK
                                    )
                      else:
                            print("no buttion is clicked")
                            return Response(
                              {
                                    "msg":"no buttion is clicked"    

                              },
                               status=status.HTTP_400_BAD_REQUEST

                              )
            else:
                  print("product ids is not available")
                  return Response({
                        "msg":"product ids is not received"
                  },
                   status=status.HTTP_400_BAD_REQUEST
                  )
def delete_page(request):
      print("inside the delete page")
      return render(request,"delete_inventry.html")
                           
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
            product_id=request.data.get("product_id")
            cart_product_ids = request.session.get(
                  "cart_product_ids", []
            )
            # Add the new product ID
            if product_id not in cart_product_ids:
                  cart_product_ids.append(product_id)


            # Save the updated list in the session
            print("product ids enterd in cart_ids")
            request.session["cart_product_ids"] = cart_product_ids
            return Response(
                  {
                  "msg":"product id added succesfully in session"
                  },
                  status=status.HTTP_201_CREATED

            )



            # search filter 
            # searchvalue=request.data.get("searchvalue")
            # print(searchvalue)
            # products=product_data.objects.all().filter(product_name=searchvalue)
            # print(products)  
            # if products:
            #      print("products is available")
            #      return Response({
            #          "products":products
            #       },
            #       status=status.HTTP_200_OK
            #       )
            # else:
            #     print("products is not available")
            #     return Response({
            #           "msg":"This product is not available"
            #     },
            # #     status=status.HTTP_400_BAD_REQUEST
            #     )
# class Add_CartAPIView(APIView):
#        def get(self, request):
#             print("get the request in addcart")
#             product_id = request.query_params.get("product_id")
#             print(product_id)
#             if not product_id:
#                   print("product id not have value")
#                   return Response(
#                       {"error": "Product ID is required"},
#                       status=status.HTTP_400_BAD_REQUEST
#                   )
#                   # Retrieve the product from the database
#             cart_product_ids = request.session.get(
#                   "cart_product_ids", []
#             )
#             # Add the new product ID
#             if product_id not in cart_product_ids:
#                   cart_product_ids.append(product_id)

#             # Save the updated list in the session
#             request.session["cart_product_ids"] = cart_product_ids
#             return Response({
#                   "message": "Product added to cart successfully",
      
      #   }, status=status.HTTP_200_OK)
      # 
class cartpageAPIView(APIView):
      def get(self, request):
            print("get inside the cart page")
            cart_product_ids = request.session.get("cart_product_ids", [])
            cart_items=[]
            total_prices=[]
            if cart_product_ids:
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
                  print("cartitems is fatched")
                  len_of_cart=len(cart_items)
                  subtotal=0
                  for total_price in total_prices:
                        subtotal+=total_price
                  delivery_charges=subtotal*1/100
                  total_amount=subtotal+delivery_charges
                  request.session["subtotal"] = subtotal
                  request.session["delivery_charges"] = delivery_charges
                  request.session["total_amount"] = total_amount
                  print("st,dc,TA is calculated")
                  return render(
                              request,"cart.html",
                        { "cart_items":cart_items ,"total_prices":total_prices,"len_of_cart":len_of_cart,"subtotal":subtotal,"delivery_charges":delivery_charges,"total_amount":total_amount}
                        )
            return render(request,"cart.html")
      def post(self,request):
              print("post request inside cart page")
              cartitems=request.data.get("cartitems")
              print(cartitems)
              cart_product_ids = request.session.get("cart_product_ids", [])
              if cart_product_ids:
                  request.session["order_product_ids"]=cart_product_ids 
                  print("product id is store in order ids")
                  return Response(
                        {"mag":"product is added to orders page"},
                         status=status.HTTP_200_OK
                        )
              else:
                    print("cart ids is not available ")
                    return Response(
                        {"mag":"product is added to orders page"},
                        status=status.HTTP_400_BAD_REQUEST
                        )
              

            




            #       return Response(
            #             {
            #             "cart_items":cart_items ,
            #             "total_prices":total_prices,
            #             "len_of_cart":len_of_cart,
            #             "subtotal":subtotal,
            #             "delivery_charges":delivery_charges,
            #             "total_amount":total_amount
            #       },
            #       status=status.HTTP_200_OK
            #       )
            # print("cartids not have any ids")
            # return Response({
            #       "msg":"this cart ids not have any product id"
            # })

           
class orderAPIView(APIView):
      def get(self, request):
            order_product_ids=request.session.get("order_product_ids")
            if order_product_ids:
                  subtotal=request.session.get("subtotal")
                  delivery_charges=request.session.get("delivery_charges")
                  total_amount=request.session.get("total_amount")
                  order_items = product_data.objects.filter(product_id__in=order_product_ids)
                  return render(request,"orders.html",{"order_items":order_items,"subtotal":subtotal,"delivery_charges":delivery_charges,"total_amount":total_amount})
            else:
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
