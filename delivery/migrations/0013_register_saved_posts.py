# Generated by Django 5.1.7 on 2025-03-22 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0012_rename_img_posts_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='saved_posts',
            field=models.ManyToManyField(blank=True, related_name='saved_users', to='delivery.posts'),
        ),
    ]
