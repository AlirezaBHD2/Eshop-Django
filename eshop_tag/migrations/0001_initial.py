# Generated by Django 3.1.2 on 2020-10-05 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eshop_product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='عنوان')),
                ('slug', models.SlugField(verbose_name='عنوان در url')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('active', models.BooleanField(default=True, verbose_name='فعال / غیر فعال')),
                ('products', models.ManyToManyField(blank=True, to='eshop_product.Product', verbose_name='محصولات')),
            ],
            options={
                'verbose_name': 'برچسب / تگ',
                'verbose_name_plural': 'برچسب ها / تگ ها',
            },
        ),
    ]
