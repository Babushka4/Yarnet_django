# Generated by Django 4.0.2 on 2022-03-06 07:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('regulations', '0002_alter_regulations_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='regulations',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
