# Generated by Django 3.0.8 on 2020-08-06 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newslist', '0007_auto_20200804_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='idnews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.SlugField(max_length=20000, null=True)),
                ('idtitle', models.IntegerField()),
            ],
        ),
    ]