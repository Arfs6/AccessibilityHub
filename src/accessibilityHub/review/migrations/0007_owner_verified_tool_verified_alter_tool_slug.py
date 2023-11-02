# Generated by Django 4.2.6 on 2023-11-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_alter_tool_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tool',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tool',
            name='slug',
            field=models.SlugField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
