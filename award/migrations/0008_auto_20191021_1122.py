# Generated by Django 2.2.6 on 2019-10-21 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('award', '0007_auto_20191021_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='vote_average',
            field=models.IntegerField(),
        ),
    ]
