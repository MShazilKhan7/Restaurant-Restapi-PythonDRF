from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('menu-items/', views.MenuItemsCreateView.as_view()),  
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view()), 
    path('api-token-auth/', obtain_auth_token), 
    path('manager-view/',views.manager_view),
    path("categories/", views.CategoryListCreateAPIView.as_view()),
    path('users/users/me/', views.list_current_user),
    path("cart/menu-items/", views.cart_items),
    path("orders/", views.orders),
    path('orders/<int:order>', views.order_item_list),
    path("groups/manager/users/", views.AllManagers),
    path("groups/delivery-crew/users/", views.delivery_crew)
]
