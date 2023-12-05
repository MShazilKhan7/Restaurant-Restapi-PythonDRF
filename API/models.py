from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    slug  = models.SlugField()
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT,db_index=True, null=True)
    item     = models.CharField(max_length=255, db_index=True)
    price    = models.DecimalField(max_digits=6,decimal_places=2)
    featured = models.BooleanField(db_index=True)
    
    def __str__(self):
        return self.item
    

class CartItems(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        unique_together = ("menu_item","user") 
    
            
    def __str__(self):
        return self.menu_item.item
    

class Order(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    delivery_crew   = models.ForeignKey(User, related_name='delivery_crew', on_delete=models.SET_NULL, null=True)
    date            = models.DateField(auto_now=True, )
    status          = models.BooleanField()
    total           = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.user.username
2

class OrderItem(models.Model):
    order      = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem   = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity   = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price      = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'menuitem')

    def __str__(self):
        return self.order.username