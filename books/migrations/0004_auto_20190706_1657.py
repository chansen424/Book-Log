# Generated by Django 2.2.3 on 2019-07-06 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='writer',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='books.Author'),
        ),
    ]
