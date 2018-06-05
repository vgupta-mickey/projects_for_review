from django.contrib import admin
from .models import Profile, Item, Lostitem, Founditem, Category, Address

# Register your models here.
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Item)
admin.site.register(Lostitem)
admin.site.register(Founditem)
admin.site.register(Category)
