# Generated by Django 5.1.2 on 2025-01-09 22:54

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_alter_event_title'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
