# Generated by Django 5.1.2 on 2024-11-17 08:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='session_year',
            new_name='session_year_id',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='subject',
            new_name='subject_id',
        ),
        migrations.RenameField(
            model_name='attendancereport',
            old_name='attendance',
            new_name='attendance_id',
        ),
        migrations.RenameField(
            model_name='attendancereport',
            old_name='student',
            new_name='student_id',
        ),
        migrations.RenameField(
            model_name='feedbackstaffs',
            old_name='staff',
            new_name='staff_id',
        ),
        migrations.RenameField(
            model_name='feedbackstudent',
            old_name='student',
            new_name='student_id',
        ),
        migrations.RenameField(
            model_name='leavereportstaff',
            old_name='staff',
            new_name='staff_id',
        ),
        migrations.RenameField(
            model_name='leavereportstudent',
            old_name='student',
            new_name='student_id',
        ),
        migrations.RenameField(
            model_name='notificationstaffs',
            old_name='staff',
            new_name='staff_id',
        ),
        migrations.RenameField(
            model_name='notificationstudent',
            old_name='student',
            new_name='student_id',
        ),
        migrations.RenameField(
            model_name='studentresult',
            old_name='student',
            new_name='student_id',
        ),
        migrations.RenameField(
            model_name='studentresult',
            old_name='subject',
            new_name='subject_id',
        ),
        migrations.RenameField(
            model_name='students',
            old_name='course',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='students',
            old_name='session_year',
            new_name='session_year_id',
        ),
        migrations.RenameField(
            model_name='subjects',
            old_name='staff',
            new_name='staff_id',
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='course',
        ),
        migrations.AddField(
            model_name='subjects',
            name='course_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.courses'),
        ),
        migrations.AlterField(
            model_name='adminhod',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='adminhod',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='attendancereport',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courses',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('1', 'HOD'), ('2', 'Staff'), ('3', 'Student')], default=1, max_length=10),
        ),
        migrations.AlterField(
            model_name='feedbackstaffs',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='feedbackstudent',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='leavereportstaff',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='leavereportstudent',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notificationstaffs',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notificationstudent',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='students',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='students',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
