# Generated by Django 3.1.6 on 2021-06-21 10:56

import UserApp.models
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.CharField(db_index=True, max_length=10, unique=True)),
                ('category_name', models.CharField(db_index=True, max_length=20, unique=True)),
                ('category_image_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dummy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('location', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_id', models.CharField(db_index=True, max_length=10, unique=True)),
                ('location_name', models.CharField(db_index=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(db_index=True, max_length=10, unique=True)),
                ('service_name', models.CharField(db_index=True, max_length=300)),
                ('service_description', models.CharField(max_length=500)),
                ('service_image_name', models.CharField(max_length=100)),
                ('service_providers', django_mysql.models.ListCharField(models.CharField(max_length=100), default=list, max_length=99999, size=None)),
                ('service_visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('user_id', models.CharField(db_index=True, max_length=10, unique=True)),
                ('contact_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MaxLengthValidator(10), django.core.validators.MinLengthValidator(10)])),
                ('name', models.CharField(max_length=200)),
                ('user_type', models.IntegerField(default=3)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProviders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_id', models.CharField(db_index=True, max_length=10, unique=True)),
                ('provider_name', models.CharField(db_index=True, max_length=300)),
                ('provider_number', models.CharField(max_length=10, validators=[UserApp.models.validate_phone])),
                ('provider_image_name', models.CharField(default='default.jpg', max_length=100)),
                ('provider_bio', models.CharField(default='No Bio', max_length=500)),
                ('provider_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.locations')),
                ('provider_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.services')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(db_index=True, max_length=10, unique=True)),
                ('order_services', django_mysql.models.ListCharField(models.CharField(max_length=300), default=list, max_length=99999, size=None)),
                ('order_total_bill', models.FloatField(default=0)),
                ('order_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.userprofile')),
            ],
        ),
    ]
