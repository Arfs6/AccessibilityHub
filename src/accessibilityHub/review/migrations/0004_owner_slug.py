# Generated by Django 4.2.6 on 2023-10-28 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_alter_review_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='slug',
            field=models.SlugField(default='', max_length=6),
            preserve_default=False,
        ),
    ]
