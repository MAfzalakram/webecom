from django.contrib import admin
from .models import Catagory, Customer, Product, Order, Profile
from django.contrib.auth. models import User

# Simple registration
admin.site.register(Catagory)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


class ProfileInLine(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInLine]



admin.site.unregister(User)
admin.site.register(User, UserAdmin)