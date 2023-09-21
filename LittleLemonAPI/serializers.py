
from rest_framework import serializers 
from .models import MenuItem,Cart,Order,Category,OrderItem
from rest_framework.validators import UniqueTogetherValidator 
from django.contrib.auth.models import User,Group 

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
 def validate(self, attrs):
  if(attrs['price']<2):
   raise serializers.ValidationError('Price should not be less than 2.0')
  return super().validate(attrs)
 class Meta:
        model = MenuItem
        fields = ["id","title","price","featured","category"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
     model = Cart
     fields = ['id','user','menuitem','quantity','unit_price','price']


class OrderSerializer(serializers.ModelSerializer):
 class Meta:
  model = Order
  fields = ['id','user','delivery_crew','status','total','date']


class OrderItemSerializer(serializers.ModelSerializer):
 class Meta:
  model = OrderItem
  fields = ['id' ,'order','menuitem','quantity','unit_price','price']

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = []
class UserSerializer(serializers.ModelSerializer): # Clasa User trebuie sa aiba prorpiul serializer
     
    class Meta:
        model = User
        fields = ['id','username']