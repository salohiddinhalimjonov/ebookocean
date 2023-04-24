from django.contrib import admin
from src.order.models import *
# Register your models here.

admin.site.register([Order, Discount])