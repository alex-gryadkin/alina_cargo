# Generated by Django 4.2 on 2023-04-16 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_alter_userpackages_desc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='packages',
            options={'verbose_name_plural': 'Трек-номера'},
        ),
        migrations.AlterModelOptions(
            name='userpackages',
            options={'verbose_name_plural': 'Трек-номера пользователей'},
        ),
        migrations.AlterField(
            model_name='packages',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Трек'),
        ),
        migrations.AlterField(
            model_name='packages',
            name='status',
            field=models.CharField(choices=[('new', '📝 Добавлен'), ('eha', '🚚 В пути'), ('tut', '🗿 Ожидает'), ('vse', '🤝 Выдан')], default='new', max_length=3, verbose_name='Статус'),
        ),
    ]
