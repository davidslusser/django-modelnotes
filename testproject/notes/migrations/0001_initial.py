# Generated by Django 2.2.17 on 2021-01-19 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import notes.models


def load_initial_data(apps, schema_editor):
    Scope = apps.get_model('notes', 'Scope')

    scope_list = [
        {'name': 'private', 'description': 'only the author can access'},
        {'name': 'group', 'description': 'any member of an assigned group can access'},
        {'name': 'public', 'description': 'accessible to everyone'},
    ]
    for i in scope_list:
        Scope.objects.get_or_create(**i, defaults=i)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='title for this note', max_length=32)),
                ('content', models.TextField(help_text='the actual content of this note')),
                ('object_id', models.PositiveIntegerField()),
                ('object_repr', models.CharField(blank=True, help_text='string representation of an object instance', max_length=128, null=True)),
                ('author', models.ForeignKey(blank=True, help_text='user who created this note', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('groups', models.ManyToManyField(blank=True, through='notes.GroupPermission', to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='permission', max_length=16, unique=True)),
                ('description', models.CharField(help_text='description of this permission', max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='name of this scope', max_length=16, unique=True)),
                ('description', models.CharField(help_text='description of this scope', max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Note')),
                ('permission', models.ForeignKey(blank=True, help_text='actions that can be performed on a public scoped note', null=True, on_delete=django.db.models.deletion.SET_NULL, to='notes.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='note',
            name='public_permissions',
            field=models.ManyToManyField(blank=True, help_text='indicated actions that can be performed on this note when scope is set to public', through='notes.PublicPermission', to='notes.Permission'),
        ),
        migrations.AddField(
            model_name='note',
            name='scope',
            field=models.ForeignKey(blank=True, default=notes.models.get_default_scope, help_text='sets access to this note', null=True, on_delete=django.db.models.deletion.SET_NULL, to='notes.Scope'),
        ),
        migrations.AddField(
            model_name='grouppermission',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Note'),
        ),
        migrations.AddField(
            model_name='grouppermission',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text='actions that can be performed on a group scoped note', to='notes.Permission'),
        ),

        migrations.RunPython(load_initial_data)
    ]
