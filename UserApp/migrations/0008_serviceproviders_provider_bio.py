# Generated by Django 3.1.6 on 2021-06-03 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_auto_20210603_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceproviders',
            name='provider_bio',
            field=models.CharField(default='No Bio', max_length=500),
        ),
    ]
