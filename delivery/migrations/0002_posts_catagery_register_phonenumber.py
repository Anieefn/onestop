# Generated by Django 5.1.7 on 2025-03-17 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='catagery',
            field=models.CharField(default='shirts', max_length=13),
        ),
        migrations.AddField(
            model_name='register',
            name='phonenumber',
            field=models.CharField(default=1, max_length=10),
        ),
    ]
