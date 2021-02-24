from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=12, unique=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    SOLDOUT = (
        (0, '通常販売'),
        (1, '売り切れ中')
    )
    name = models.CharField('料理名', max_length=36)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='料理カテゴリ',related_name='menus')
    price = models.IntegerField('価格')
    text = models.TextField('特記事項やアレルギー等', blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    soldout = models.IntegerField('販売状況', choices=SOLDOUT, blank=True, null=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField('住所', max_length=64)
    shippingtax = models.IntegerField('送料')
    shippingtime = models.IntegerField('配達所要時間(分)')
    mustorderprice = models.IntegerField('必要注文最低額')

    def __str__(self):
        return self.name

class ChoiceLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name='住所', default=1)

    def __str__(self):
        return self.location
