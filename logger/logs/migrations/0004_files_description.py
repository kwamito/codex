# Generated by Django 3.0.6 on 2020-05-30 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_comment_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='description',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
