# Generated by Django 5.1.7 on 2025-03-24 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0014_alter_posts_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='bio',
            field=models.CharField(max_length=2000),
        ),
    ]
