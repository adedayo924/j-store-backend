# Generated by Django 4.2.5 on 2023-10-02 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.IntegerField(),
        ),
    ]
