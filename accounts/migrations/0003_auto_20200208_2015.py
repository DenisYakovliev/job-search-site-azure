# Generated by Django 3.0.3 on 2020-02-08 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200206_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
