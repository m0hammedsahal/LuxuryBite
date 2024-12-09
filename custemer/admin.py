from django.contrib import admin

from custemer.models import *

admin.site.register(Customer)
admin.site.register(Cart)

admin.site.register(Order)
admin.site.register(OrderItem)