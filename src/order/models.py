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
    user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE, related_name='orders')
    ebook = models.ForeignKey('ebook.EbookModel', on_delete=models.SET_NULL, null=True)

