# Generated by Django 3.1 on 2020-08-10 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200810_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
