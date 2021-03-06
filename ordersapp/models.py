from django.db import models
from django.conf import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    created_at = models.DateTimeField(
        verbose_name = 'создан',
        auto_now_add = True
    )

    updated_at = models.DateTimeField(
        verbose_name = 'обновлен',
        auto_now = True
    )

    status = models.CharField(
        verbose_name = 'статус',
        max_length = 3,
        choices = ORDER_STATUS_CHOICES,
        default = FORMING
    )
    is_active = models.BooleanField(verbose_name = 'активен', default = True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created_at',)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(item.quantity for item in _items)

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        return sum(item.quantity * item.product.price for item in _items)

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name = "orderitems",
        on_delete = models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        verbose_name = 'продукт',
        on_delete = models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name = 'количество',
        default = 0
    )

    def get_product_cost(self):
        return self.product.price * self.quantity


    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()