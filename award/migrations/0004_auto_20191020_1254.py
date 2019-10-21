# Generated by Django 2.2.6 on 2019-10-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('award', '0003_project_collaborators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tag',
            field=models.ManyToManyField(related_name='tags', to='award.Tag'),
        ),
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(related_name='technologies', to='award.Technology'),
        ),
    ]