from django.db import models

# Create your models here.
class Product(models.Model):
    PRODUCT_CHOICES = (
        ('FRUIT', 'fruit'),
        ('VEGETABLE', 'vegetable'),
    )
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=12, choices=PRODUCT_CHOICES, default='FRUIT')
    price = models.FloatField(default=100.0)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} : {self.price}'