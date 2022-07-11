# Generated by Django 4.0.6 on 2022-07-08 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('others', models.TextField(null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]