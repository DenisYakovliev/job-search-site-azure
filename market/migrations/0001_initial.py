# Generated by Django 3.0.3 on 2020-02-06 11:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20200206_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='title')),
                ('slug', models.SlugField()),
                ('salary', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField()),
                ('location', models.CharField(blank=True, max_length=100)),
                ('type', models.CharField(blank=True, choices=[('1', 'Full time'), ('2', 'Part time'), ('3', 'Internship')], max_length=10)),
                ('category', models.CharField(blank=True, choices=[('1', 'Web design'), ('2', 'Graphic design'), ('3', 'Web developer'), ('4', 'Human Resources'), ('5', 'Software Developer')], max_length=100)),
                ('last_date', models.DateTimeField()),
                ('website', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('filled', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
            options={
                'verbose_name_plural': 'Jobs',
                'ordering': ['-created_at'],
            },
        ),
    ]
