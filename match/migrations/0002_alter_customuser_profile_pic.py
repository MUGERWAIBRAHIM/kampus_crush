# Generated by Django 5.2 on 2025-04-10 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.CharField(blank=True, default=None, max_length=2083, null=True),
        ),
    ]
