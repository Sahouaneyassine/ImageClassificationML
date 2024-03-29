# Generated by Django 3.1.5 on 2021-01-18 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('photo', models.ImageField(upload_to='photos')),
            ],
        ),
    ]
