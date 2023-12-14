from django.contrib import admin
from .models import Product, MyUser


class MemberAdmin(admin.ModelAdmin):
    list_display = ("title", "price")
    prepopulated_fields= {"slug":("title", "price")}


admin.site.register(Product, MemberAdmin)
admin.site.register(MyUser)

