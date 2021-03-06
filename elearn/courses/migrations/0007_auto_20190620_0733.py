# Generated by Django 2.0.5 on 2019-06-20 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20190615_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='module',
            field=models.ForeignKey(limit_choices_to={'model__in': ('texts', 'files', 'images', 'videos')}, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.Module'),
        ),
    ]
