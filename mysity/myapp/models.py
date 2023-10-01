from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    phone = models.CharField(max_length=20, blank=False, verbose_name='Телефон')
    address = models.CharField(max_length=250, blank=False, verbose_name='Адрес')


class MenuCategories(models.Model):
    categorie = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    queue = models.IntegerField(verbose_name='Очередность категории')

    class Meta:
        db_table = 'menu_categories'
        verbose_name = 'категорию '
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.categorie

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Products(models.Model):
    image = models.ImageField(upload_to='static/image/%Y/%m/%d/', verbose_name='Изображение')
    product_name = models.CharField(max_length=50, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(verbose_name='Полное описание')
    price = models.IntegerField(verbose_name='Цена')
    menu_categories = models.ManyToManyField(MenuCategories, verbose_name='Категория товара')
    product_quantity = models.IntegerField(verbose_name='Количество товара')
    queue = models.IntegerField(editable=False, default=0, verbose_name='Очередность')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    publication = models.BooleanField(default=True, verbose_name='Опубликовано')

    # метаданные для модели
    class Meta:
        db_table = 'products'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['id']

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product', kwargs={'post_slug': self.slug})


class Orders(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name='Покупатель')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    delivered = models.BooleanField(default=False, verbose_name='Доставлен')

    class Meta:
        ordering = ('-created',)
        db_table = 'orders'
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, editable=False, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_items',
                                verbose_name='Наименование заказа')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кол-во')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'товар'
        verbose_name_plural = 'покупки'

    def __str__(self):
        return format(self.product)

    def get_cost(self):
        return self.price * self.quantity

