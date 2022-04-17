# Generated by Django 4.0 on 2021-12-25 14:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votefact',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='votefact',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user'),
        ),
        migrations.AlterField(
            model_name='votefact',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.votevariant'),
        ),
        migrations.AlterField(
            model_name='votevariant',
            name='description',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='votevariant',
            name='voting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.voting'),
        ),
        migrations.AlterField(
            model_name='voting',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.user'),
        ),
        migrations.AlterField(
            model_name='voting',
            name='description',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='voting',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='voting',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]