# Generated by Django 2.2.3 on 2019-07-09 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20190708_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.AddField(
            model_name='book',
            name='image_url',
            field=models.URLField(default='https://previews.123rf.com/images/eljanstock/eljanstock1811/eljanstock181107013/113550870-book-concept-line-icon-linear-book-concept-outline-symbol-design-this-simple-element-illustration-ca.jpg'),
        ),
    ]
