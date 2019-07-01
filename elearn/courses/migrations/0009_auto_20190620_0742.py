# Generated by Django 2.0.5 on 2019-06-20 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20190620_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('text', 'file', 'image', 'video')}, on_delete=django.db.models.deletion.CASCADE, related_name='content_type', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='content',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.Module'),
        ),
    ]
