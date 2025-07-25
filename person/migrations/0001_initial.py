# Generated by Django 5.1.1 on 2025-07-21 10:40

import django.core.validators
import django.db.models.deletion
import person.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_person', models.IntegerField(choices=person.models.Choices.event_person_choices, default=1, verbose_name='पदाधिकारी/कर्मचारी')),
                ('name', models.CharField(max_length=200)),
                ('ev_date', models.DateField(verbose_name='Event_Date')),
                ('str_date', models.CharField(max_length=15, null=True, verbose_name='कार्यक्रम मिति')),
                ('event_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('event_location', models.CharField(max_length=300, null=True, verbose_name='कार्यक्रम स्थान')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='पदनाम')),
                ('post_for', models.IntegerField(blank=True, choices=person.models.Choices.catagory, default=1, null=True)),
            ],
            options={
                'verbose_name': 'पद',
                'verbose_name_plural': 'पदहरु',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.IntegerField(choices=person.models.Choices.male_female_choices, default=1, null=True, verbose_name='लिङ्ग')),
                ('mobile_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='invalid_mobile_number', message='मोबाइल नंबर १० अङ्कको हुनुपर्छ र ९ बाट सुरु भएको', regex='^9[0-9]{9}$')], verbose_name='सम्पर्क नं')),
                ('email', models.EmailField(default='hello@example.com', max_length=254, null=True, verbose_name='ईमेल')),
                ('status', models.IntegerField(choices=person.models.Choices.StatusChoices, default=1)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('weight', models.IntegerField(choices=person.models.Choices.IntegerChoices100, default=1)),
                ('post', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='%(class)s_personalinfo', to='person.post')),
            ],
            options={
                'verbose_name': 'कर्मचारि',
                'verbose_name_plural': 'कर्मचारिहरु',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='PublicRepresentative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.IntegerField(choices=person.models.Choices.male_female_choices, default=1, null=True, verbose_name='लिङ्ग')),
                ('mobile_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='invalid_mobile_number', message='मोबाइल नंबर १० अङ्कको हुनुपर्छ र ९ बाट सुरु भएको', regex='^9[0-9]{9}$')], verbose_name='सम्पर्क नं')),
                ('email', models.EmailField(default='hello@example.com', max_length=254, null=True, verbose_name='ईमेल')),
                ('status', models.IntegerField(choices=person.models.Choices.StatusChoices, default=1)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('weight', models.IntegerField(choices=person.models.Choices.IntegerChoices100, default=1)),
                ('ward', models.IntegerField(choices=person.models.Choices.WardChoices, default=1, verbose_name='वडा')),
                ('cabinet_member', models.BooleanField(verbose_name='कार्यपालिका सदस्य')),
                ('post', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='%(class)s_personalinfo', to='person.post')),
            ],
            options={
                'verbose_name': 'जनप्रतिनिधि',
                'verbose_name_plural': 'जनप्रतिनिधिहरु',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='शाखा')),
                ('head', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headed_section', to='person.employee', verbose_name='शाखा प्रमुख')),
            ],
            options={
                'verbose_name': 'शाखा',
                'verbose_name_plural': 'शाखाहरु',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='section',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='person.section', verbose_name='शाखा'),
        ),
        migrations.CreateModel(
            name='SubjectCommittee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='विषयगत समितिको नाम')),
                ('coordinator', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coordinated_committee', to='person.publicrepresentative', verbose_name='समिति संयोजक')),
                ('members', models.ManyToManyField(blank=True, related_name='involved_committees', to='person.publicrepresentative', verbose_name='सदस्य हरु')),
                ('secretary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='committes_secretary', to='person.employee', verbose_name='सदस्य सचिव')),
            ],
            options={
                'verbose_name': 'विषयगत समिति',
                'verbose_name_plural': 'विषयगत समितिहरु',
                'ordering': ['coordinator'],
            },
        ),
    ]
