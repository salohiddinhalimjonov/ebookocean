from django.db import models
from src.common.models import BaseModel


class Discount(BaseModel):
    ebooks = models.ManyToManyField('ebook.EbookModel', related_name='discounts', blank=True)
    name = models.CharField(max_length=100)
    percent = models.PositiveSmallIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)

class Order(BaseModel):
    NEW = 'new'
    PAID = 'paid'

    STATUS = (
        (NEW, NEW),
        (PAID, PAID),
    )

    user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS, default=NEW)
    total_price = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=21, decimal_places=2, null=True)
    price_to_paid = models.DecimalField(max_digits=21, decimal_places=2, null=True)


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ebooks')
    ebook = models.ForeignKey('ebook.EbookModel', on_delete=models.CASCADE, related_name='order_ebooks')
