# Generated by Django 2.2.3 on 2019-07-09 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20190706_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.CharField(default='This book has no summary.', max_length=300),
        ),
    ]