from django.shortcuts import render,get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from .models import Category,MenuItem,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,CartSerializer,OrderSerializer,CategorySerializer,OrderItemSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User,Group
from rest_framework.authentication import TokenAuthentication


class MenuItemView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ["price","category__title"]
    search_fields = ['title',"category__title"] 
    def get_permissions(self):
     if self.request.method in ['GET']:
            return [IsAuthenticated()]  # Allow authenticated users to list menu items
     else:
            return [IsAdminUser()]   

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
 queryset = MenuItem.objects.all()
 serializer_class = MenuItemSerializer
 def get_permissions(self):
  if self.request.method in ['GET']:
            return [IsAuthenticated()]  # Allow authenticated users to list menu items
  else:
            return [IsAdminUser()]    

class CartView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class =  CartSerializer

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])

    def list(self, request, *args, **kwargs): #Am suprascris metoda list pentru a return doar comenziile cu acelasi user ID
        current_user = request.user
        cart_items = Cart.objects.filter(user=current_user.id)

        if cart_items.exists():
            serialized_items = self.serializer_class(cart_items, many=True)
            return Response({"items": serialized_items.data})
        else:
            return Response({"items": []})

    def delete(self, request, *args, **kwargs):
        current_user = request.user
        cart_items = Cart.objects.filter(user=current_user.id)
        
        if cart_items.exists():
            cart_items.delete()
            return Response({"message": "All cart items deleted for the current user"})
        else:
            return Response({"message": "No cart items to delete for the current user"})
      

class OrderItemView(generics.ListCreateAPIView,generics.DestroyAPIView):
 queryset = OrderItem.objects.all()
 serializer_class = OrderItemSerializer
 @authentication_classes([TokenAuthentication])
 @permission_classes([IsAuthenticated])

 

 class OrderItemView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        current_user = request.user

        # Step 1: Retrieve current cart items for the user
        cart_items = Cart.objects.filter(user=current_user)

        if cart_items.exists():
            # Step 2: Add cart items to the order items table
            order_items = []
            for cart_item in cart_items:
                order_item = OrderItem(
                    order=cart_item.user,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    price=cart_item.price,
                    # You may need to adjust fields as per your models
                )
                order_items.append(order_item)
            OrderItem.objects.bulk_create(order_items)

            # Step 3: Delete all items from the cart for this user
            cart_items.delete()

            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No items in the cart to create an order"}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
         current_user = request.user

        # Filter orders to show only those made by the current user
         orders = OrderItem.objects.filter(order=current_user.id)

         if orders.exists():
            serialized_items = self.serializer_class(orders, many=True)
            return Response({"orders": serialized_items.data})
         
         elif self.request.method == 'GET' and IsAdminUser.has_permission(self, request):
            # This part can be adjusted based on your requirements for admin access
            new_orders = OrderItem.objects.all()
            serialized_items = self.serializer_class(new_orders, many=True)
            return Response({'message': serialized_items.data})
         else:
            return Response({"orders": []})     
     
     

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
     if self.request.method in ['GET']:
            return [IsAuthenticated()]  # Allow authenticated users to list menu items
     else:
            return [IsAdminUser()]  
     

class OrderView(generics.RetrieveUpdateDestroyAPIView,generics.ListCreateAPIView):
   queryset = Order.objects.all()
   serializer_class = OrderSerializer
   
   @authentication_classes([TokenAuthentication])
   @permission_classes([IsAuthenticated])

   def list(self, request, *args, **kwargs):
       current_user = request.user
       orders = Order.objects.filter(user=current_user.id)

       if (orders.exists() and current_user.id):
         serialized_items = self.serializer_class(orders, many=True)
         return Response({"orders": serialized_items.data})
     
       elif ( self.request.method in ['GET'] and permission_classes([IsAdminUser]) ):
        new_orders = Order.objects.all()
        serialized_items = self.serializer_class(new_orders, many=True)
        return Response({'message': serialized_items.data})
      
       else:
          return Response({"orders": []})
     


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers_function(request):
    if request.method == 'GET':
        managers_group = Group.objects.get(name="Managers") #In acest caz, variabila managers_group trebuie sa fie inclusa in scopul structurii de decizie if deoarece, pentru a afisa toti manageri la efectuarea unei cererii HTTP GET, aceasta variabila va retine la fiecare parcurgere obiectele din groupul Manager
        managers_users = managers_group.user_set.all()
        serializer = UserSerializer(managers_users, many=True)
        return Response({'managers': serializer.data})

    username = request.data.get('username')
    user = get_object_or_404(User, username=username)
    managers_group = Group.objects.get(name="Managers")

    if request.method == 'POST':
        managers_group.user_set.add(user)
        return Response({'message': 'User added to manager group'})

    elif request.method == 'DELETE':
        managers_group.user_set.remove(user)
        return Response({'message': 'User removed from the manager group'})
    
    return Response({'message': 'Invalid request'})

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def delivery_function(request):
    
    if  request.method == 'GET'  :
        delivery_group = Group.objects.get(name='Delivery crew')
        delivery_users = delivery_group.user_set.all()
        serializer = UserSerializer(delivery_users, many=True)
        return Response({'delivery_crew': serializer.data})
    
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        delivery_group = Group.objects.get(name='Delivery crew')
        delivery_group.user_set.add(user)
        return Response({"message": 'User added to the delivery crew group'})
    
    if request.method == 'DELETE':
        delivery_group = Group.objects.get(name='Delivery crew')
        delivery_group.user_set.remove(user)
        return Response({"message":"User removed from the delivery crew group"})

    return Response({'message': 'Invalid request'})


 