from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from django.http import request,HttpResponseForbidden
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .models import MenuItem,Category,Order,OrderItem,CartItems,Category
from rest_framework import generics
from .serializers import MenuItemSerializer, CartItemSerializer,CreateUserSerializer,UserSerializer,OrderSerializer, AllOrdersSerializer, CategorySerializer
from urllib.parse import quote
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User,Group
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
user = get_user_model()


class Pagination(PageNumberPagination):
    page_size = 4

class MenuItemsCreateView(generics.ListCreateAPIView):
    queryset         = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends  = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category']
    ordering_fields  = ['price']
    pagination_class = Pagination
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message":"Only admin can add items"})
        return super().post(request, *args, **kwargs)
    
   
    
# Menu Items handling
class SingleMenuItem(generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):  
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) 
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'detail': 'You do not have permission to add menu items.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'detail': 'You do not have permission to update menu items.'}, status=status.HTTP_403_FORBIDDEN)
        return super().put(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'detail': 'You do not have permission to delete menu items.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Managers').exists():
            Response({'detail': 'You do not have permission to patch menu items.'}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)
    
    

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        cart_item  = CartItems.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_item, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        user = request.user

        menu_item_id = request.data.get('menuitem')
        quantity = request.data.get('quantity')

        try: 
            menu_item = MenuItem.objects.get(id=menu_item_id)
            
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item does not exist.'}, status=status.HTTP_404_NOT_FOUND)
      
        unit_price = menu_item.price
        price = unit_price*quantity
        
        user_cart = Cart.objects.get(user=user.id)
        cart_item=CartItems(user=user_cart, menu_item=menu_item, quantity=quantity, unit_price=unit_price, price=price)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method =='DELETE':
        CartItems.objects.filter(user=request.user).delete()
        return Response({'messege':'Items Deleted'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Managers').exists():
        return Response({"message":"only manager should see this"})
    else:
        return Response({"messge":"You are not authorized user"}, 403)


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Managers")
        if  request.method == 'POST':
            managers.user_set.add(user)
            return Response({"message":f"{username} added to the manager group"})
        elif request.method == 'DELETE':
            managers.user_set.remove(user) 
            return Response({"message":f"{username} removed to the manager group"})
    return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



# managers
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def AllManagers(request):
    if request.method == 'GET':
        if not request.user.is_staff:
            return Response({"message":"only Admin can see managers"})
    
        else:
            group   = Group.objects.get(name='Managers')
            members = User.objects.filter(groups=group)
            members = UserSerializer(members, many=True)
            return Response(members.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        if not request.user.is_staff:
            return Response({"message":"only Admin can add managers"})
       
        else:
            username = request.data['username']
            user = User.objects.get(username=username)
            if user.groups.filter(name='Managers').exists():
                return Response({"message":"Already exists"})
            else:
                managers = Group.objects.get(name="Managers")
                managers.user_set.add(user)
                return Response({"message":f"{username} added to the manager group"}, status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if request.method == 'POST':
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'detail': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        username = request.data['username']
        user     = User.objects.get(username=username)
        delivery    = Group.objects.get(name='Delivery_crew')
        delivery.user_set.add(user)
        return Response({"message":f"{username} added to the Delivery crew group"}, status=status.HTTP_201_CREATED)
        
        
# order management handles orders/
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def orders(request):
    if request.method == 'GET':
        if not request.user.groups.filter(name='Managers').exists():
            user = request.user
            orders = OrderItem.objects.filter(order=user)
            if orders:
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"messege":"No orders"}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = OrderItem.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        cart_id = Cart.objects.get(user=request.user.id).id
        user = request.user
        total = 0
        cart_items = CartItems.objects.filter(cart=cart_id)
        if cart_items:
            for items in cart_items:
                OrderItem.objects.create(order=user, menuitem=items.menu_item, quantity=items.quantity, unit_price=items.unit_price, price=items.price)
                print(items.price)
                total += items.price
            Order.objects.create(user=user, status=0, delivery_crew=None,total=total)
            cart_items.delete()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Order Created"},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET', 'PUT','DELETE','PATCH'])
@permission_classes([IsAuthenticated])
def order_item_list(request, order):
    if request.method == 'GET':
        if not request.user.groups.filter(name='Managers').exists() and request.user.id:
            items_ordered = OrderItem.objects.filter(order=order)
            serializer = OrderSerializer(items_ordered, many=True)
            if serializer.data:
                return Response(serializer.data)
            else:
                return Response({"message":"No orders"})
                
        else:
            return Response({"message": "Invalid User"}, status=status.HTTP_403_FORBIDDEN)

        order_items = OrderItem.objects.all()
        serializer = OrderSerializer(order_items, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({"message":"No orders"})
        
  
    elif request.method == 'DELETE':
        if not request.user.groups.filter(name='Managers').exists() and order==request.user.id:
            return Response({"message":"You Cannot delete Orders"}, status=status.HTTP_403_FORBIDDEN)
        
        OrderItem.objects.filter(order=order).delete()
        return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if not request.user.groups.filter(name='Managers').exists() and order==request.user.id:
            return Response({"message":"only managers have permissions"}, status=status.HTTP_403_FORBIDDEN)
        
        order = Order.objects.get(user=order)
        serializer = AllOrdersSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
    elif request.method == 'PATCH':
        serializer = AllOrdersSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
class CreateUser(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    def create_user(request):
        serialized_user = CreateUserSerializer(data=request.data)
        if serialized_user.is_valid():
            user = serialized_user.save()
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_current_user(request):
    print('Current username:', request.user.username)
    queryset = User.objects.filter(username=request.user.username)
    serializer = ShowUserSerializer(queryset, many=True)
    print('Filtered queryset:', serializer.data)
    return Response(serializer.data)
    
