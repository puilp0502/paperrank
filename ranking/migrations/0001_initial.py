# Generated by Django 2.0.3 on 2018-05-27 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('slug', models.SlugField(blank=True)),
                ('author', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('abstract', models.TextField(blank=True)),
                ('score', models.FloatField()),
                ('registered', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ranking.Publisher'),
        ),
    ]