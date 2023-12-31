# Generated by Django 4.2.7 on 2023-11-30 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import library.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=30)),
                ('isbn', models.PositiveIntegerField()),
                ('autor', models.CharField(max_length=40)),
                ('categorie', models.CharField(choices=[('educatie', 'Educație'), ('divertisment', 'Divertisment'), ('benzi desenate', 'Benzi desenate'), ('biografie', 'Biografie'), ('istorie', 'Istorie'), ('roman', 'Roman'), ('fantezie', 'Fantezie'), ('thriller', 'Thriller'), ('romantic', 'Romantic'), ('stiinta-fictiune', 'Științifico-fantastic')], default='education', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facultate', models.CharField(max_length=30)),
                ('isbn', models.CharField(max_length=30)),
                ('data_emitere', models.DateField(auto_now=True)),
                ('data_expirare', models.DateField(default=library.models.get_expiry)),
            ],
        ),
        migrations.CreateModel(
            name='StudentExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facultate', models.CharField(max_length=40)),
                ('specializare', models.CharField(max_length=40)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
