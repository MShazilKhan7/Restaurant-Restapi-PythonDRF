from django.contrib import admin
from API.models import MenuItem,Category,User,OrderItem,Order,CartItems
# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CartItems)


