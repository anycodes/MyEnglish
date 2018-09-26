# Generated by Django 2.0.4 on 2018-09-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='英文句子')),
                ('wav', models.CharField(max_length=150, verbose_name='音频路径')),
                ('chinese', models.CharField(max_length=150, verbose_name='中文翻译')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='存入时间')),
                ('remark', models.CharField(blank=True, max_length=150, null=True, verbose_name='备注说明')),
            ],
            options={
                'verbose_name': '句子背诵',
                'verbose_name_plural': '句子背诵',
                'ordering': ['-sid'],
            },
        ),
    ]
