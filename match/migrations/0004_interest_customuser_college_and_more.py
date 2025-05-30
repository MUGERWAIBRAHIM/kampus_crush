# Generated by Django 5.2 on 2025-04-11 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0003_alter_customuser_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='college',
            field=models.CharField(blank=True, choices=[('COCIS', 'COCIS'), ('CEDAT', 'CEDAT'), ('CHUSS', 'CHUSS')], max_length=10, null=True),
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='interests',
        ),
        migrations.AddField(
            model_name='customuser',
            name='interests',
            field=models.ManyToManyField(blank=True, to='match.interest'),
        ),
    ]
