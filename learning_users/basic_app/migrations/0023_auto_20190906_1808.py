# Generated by Django 2.2.1 on 2019-09-06 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0022_userprofileinfo_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='mob_no',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
