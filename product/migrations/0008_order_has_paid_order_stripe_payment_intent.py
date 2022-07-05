# Generated by Django 4.0.5 on 2022-07-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_payment_intent',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
