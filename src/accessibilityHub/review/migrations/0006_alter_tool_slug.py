# Generated by Django 4.2.6 on 2023-10-28 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_tool_slug_alter_owner_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='slug',
            field=models.SlugField(max_length=128, null=True),
        ),
    ]