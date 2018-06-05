from django.contrib import admin

from .models import Item_size, Pizza_cat, Pizza_type, Sub_type, Salad_type, Pasta_type, Dinnerplatter_type, Topping, Pizza, Subs, Salad, Pasta, Dinnerplatter, Cart, Build_pizza, Order, Build_subs, Build_pasta, Build_salad, Build_dinnerplatter

# Register your models here.

#To see the cart and order details on admin interface 
class PizzaAdminInline(admin.TabularInline):
    model = Build_pizza
    extra = 0
class SubsAdminInline(admin.TabularInline):
    model = Build_subs 
    extra = 0
class PastaAdminInline(admin.TabularInline):
    model = Build_pasta 
    extra = 0
class SaladAdminInline(admin.TabularInline):
    model = Build_salad 
    extra = 0
class DinnerplatterAdminInline(admin.TabularInline):
    model = Build_dinnerplatter 
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = (PizzaAdminInline, SubsAdminInline, PastaAdminInline, SaladAdminInline, DinnerplatterAdminInline,)

class OrderAdmin(admin.ModelAdmin):
    inlines = (PizzaAdminInline, SubsAdminInline, PastaAdminInline, SaladAdminInline, DinnerplatterAdminInline,)

admin.site.register(Item_size)
admin.site.register(Pizza_cat)
admin.site.register(Pizza_type)
admin.site.register(Pizza)
admin.site.register(Sub_type)
admin.site.register(Subs)
admin.site.register(Salad_type)
admin.site.register(Salad)
admin.site.register(Pasta_type)
admin.site.register(Pasta)
admin.site.register(Dinnerplatter_type)
admin.site.register(Dinnerplatter)
admin.site.register(Topping)
admin.site.register(Cart,CartAdmin)
admin.site.register(Build_pizza)
admin.site.register(Build_subs)
admin.site.register(Build_pasta)
admin.site.register(Build_salad)
admin.site.register(Build_dinnerplatter)
admin.site.register(Order,OrderAdmin)
