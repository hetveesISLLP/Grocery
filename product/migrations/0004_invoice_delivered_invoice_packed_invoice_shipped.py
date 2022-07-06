# Generated by Django 4.0.5 on 2022-07-04 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_review_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='delivered',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='packed',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='shipped',
            field=models.BooleanField(default=0, null=True),
        ),
    ]