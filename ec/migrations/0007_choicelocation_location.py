# Generated by Django 3.1.1 on 2020-09-20 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0006_auto_20200920_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='住所')),
                ('shippingtax', models.IntegerField(verbose_name='送料')),
                ('shippingtime', models.IntegerField(verbose_name='配達所要時間(分)')),
                ('mustorderprice', models.IntegerField(verbose_name='必要注文最低額')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ec.location', verbose_name='住所')),
            ],
        ),
    ]