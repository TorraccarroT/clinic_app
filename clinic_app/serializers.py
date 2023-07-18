from rest_framework import serializers
from .models import *

class Auction_Topic_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields ='__all__'
   

class Auction_Topic_Serializer_Status(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['sick_status']
   
class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_Product
        fields = '__all__'
   

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']
class User_Topic_Serializer(serializers.ModelSerializer):
    class Meta:
        model = clinic_user
        fields ='__all__'
   
class OrderSerializer(serializers.ModelSerializer):
    patient = User_Topic_Serializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['number', 'patient', 'items']

class Auction_Topic_Serializer_Data(serializers.ModelSerializer):
    class Meta:
        model = Save_Data
        fields ='__all__'


class Auction_Topic_Serializer_Data_1(serializers.ModelSerializer):
    class Meta:
        model = OrderReport
        fields ='__all__'