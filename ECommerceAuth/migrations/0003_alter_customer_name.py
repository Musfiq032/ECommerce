# Generated by Django 4.1.5 on 2023-01-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ECommerceAuth', '0002_customer_address_alter_customer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
