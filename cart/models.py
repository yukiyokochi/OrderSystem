from django.db import models
from ec.models import Menu
from django.utils import timezone

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)

class Payment(models.Model):
    name = models.CharField('支払い方法',max_length=255)

    def __str__(self):
        return self.name

class Form(models.Model):
    name = models.CharField('お名前', max_length=64)
    address = models.CharField('ご住所', max_length=64)
    tel = models.CharField('電話番号',max_length=255)
    email = models.EmailField('メールアドレス')
    payway = models.ForeignKey(Payment,verbose_name='支払い方法',on_delete=models.PROTECT)
    text = models.CharField('備考', max_length=512, blank=True)
    created_at = models.DateTimeField('注文日時',default=timezone.now)
    location = models.CharField('エリア',max_length=255)
    order_content = models.CharField('注文内容',max_length=512)
    totalprice = models.IntegerField()
    myself = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return self.name
