# Generated by Django 4.2.5 on 2023-09-06 15:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0004_rename_img_link_listings_imgurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='description',
            field=models.CharField(default=django.utils.timezone.now, max_length=700),
            preserve_default=False,
        ),
    ]
