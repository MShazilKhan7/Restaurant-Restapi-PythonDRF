from .models import MenuItem,Category,User,OrderItem,Order,CartItems
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class MenuItemSerializer(serializers.ModelSerializer):
   category = serializers.StringRelatedField()
   category = CategorySerializer(read_only=True)  
   category_id = serializers.IntegerField(write_only=True)                   
   class Meta:
        model = MenuItem
        fields = ['item','price','featured','category','category_id']
        
class CartItemSerializer(serializers.ModelSerializer):
   menu_items = serializers.CharField(source='menu_item')
   class Meta:
        model = CartItems
        fields = ['menu_items', 'quantity','price']
        extra_kwargs = {'price':{'read_only':True}}

class CreateUserSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True)
   class Meta:
      model = User
      fields = ('username', 'email', 'password')
      extra_kwargs = {'password':{'write_only':True}}
      
   def validate_password(self, value):
        validate_password(value)
        return value

   def create(self, validated_data):
      user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
      return user
   
class CategorySerializer(serializers.ModelSerializer):
      class Meta:
         model = Category
         fields = '__all__'
   
class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username']
      
class OrderSerializer(serializers.ModelSerializer):
   class Meta:
      model = OrderItem
      fields = ['menuitem','quantity','unit_price','price']
      extra_kwargs = {'unit_price':{'read_only':True},'price':{'read_only':True}}
class AllOrdersSerializer(serializers.ModelSerializer):
   class Meta:
      model = Order
      fields = ['user','delivery_crew', 'date','status','total']
      extra_kwargs = {'user':{'read_only':True},'total':{'read_only':True},'date':{'read_only':True}}
      