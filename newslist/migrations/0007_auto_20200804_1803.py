# Generated by Django 3.0.8 on 2020-08-04 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newslist', '0006_searchnews_urls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchnews',
            name='source',
            field=models.SlugField(max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='searchnews',
            name='title',
            field=models.SlugField(max_length=20000, null=True),
        ),
    ]
