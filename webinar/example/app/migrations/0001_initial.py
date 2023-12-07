# Generated by Django 4.2.7 on 2023-11-13 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('type', models.CharField(choices=[('FRUIT', 'fruit'), ('VEGETABLE', 'vegetable')], default='FRUIT', max_length=12)),
                ('price', models.FloatField(default=100.0)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
