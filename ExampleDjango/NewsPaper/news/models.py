from django.db import models
from datetime import datetime, timezone

# Create your models here.

class Product(models.Model): # Таблица продуктов
    name = models.CharField(max_length=255) # Название продукта
    price = models.FloatField(default=0.0) # Цена за продукт


class Staff(models.Model): # Таблица сотрудников
    # Указываем для модели Staff какие должности могут быть в БД
    director = "DI"
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.CharField(max_length=255) # ФИО сотрудника
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier) # Должность сотрудника
    labor_contract = models.IntegerField() # № трудового договора сотрудника

    def get_last_name(self): # Свойство для вывода только фамилии сотрудника
        return self.full_name.split()[0]


class Order(models.Model): # Таблица заказов
    time_in = models.DateTimeField(auto_now_add=True) # Дата оформления заказа
    time_out = models.DateTimeField(null=True) # Дата выдачи
    cost = models.FloatField(default=0.0) # Стоимость всего заказа
    pickup = models.BooleanField(default=False) # Самовывоз?
    complete = models.BooleanField(default=False) # Доставлено?
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE) # Ключ сотрудника который обрабатывал заказ

    # Связь "многие ко многим" с полем Product через промежуточную таблицу
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self): # Свойство, которое устанавливает дату выдачи заказа
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self): # Свойство возвращающее время доставки
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60


class ProductOrder(models.Model): # Промежуточная таблица
    _amount = models.IntegerField(default=1, db_column='amount') # Кол-во товаров в заказе
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Ключ продукта входящего в заказ
    order = models.ForeignKey(Order, on_delete=models.CASCADE) # Ключ заказа

    def product_sum(self): # Свойство возвращающее общую сумму за заказ
        product_price = self.product.price
        return product_price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()