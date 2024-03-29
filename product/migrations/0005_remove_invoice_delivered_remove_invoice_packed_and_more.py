# Generated by Django 4.0.5 on 2022-07-04 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_invoice_delivered_invoice_packed_invoice_shipped'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='delivered',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='packed',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='shipped',
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('Initialized', 'Initialized'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Reached Distribution Centre', 'Reached Distribution Centre'), ('Delivered', 'Delivered')], default='Initialized', max_length=30),
        ),
    ]
