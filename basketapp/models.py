from django.db import models
from authapp.models import User

from mainapp.models import Product
from ordersapp.models import OrderItem


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()

        super().delete()

class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 0)
    created_timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def baskets(self):
        return Basket.objects.filter(user = self.user)

    def total_quantity(self):
        return sum(basket.quantity for basket in self.baskets())

    def total_sum(self):
        return sum(basket.sum() for basket in self.baskets())

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk = pk).first()