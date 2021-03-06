# Generated by Django 3.0.8 on 2020-08-07 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newslist', '0010_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='mynews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.SlugField(max_length=20000, null=True)),
                ('source', models.SlugField(max_length=20000, null=True)),
                ('author', models.CharField(max_length=20000, null=True)),
                ('description', models.CharField(max_length=20000, null=True)),
                ('content', models.CharField(max_length=200000, null=True)),
                ('urls', models.CharField(max_length=200000, null=True)),
            ],
        ),
    ]
