# Generated by Django 2.2.2 on 2019-07-26 07:29

import catalog.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20190702_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='image',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=catalog.models.profile_image_upload_directory, verbose_name='저자 프로필 사진'),
        ),
    ]