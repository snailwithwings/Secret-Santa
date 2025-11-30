from django.contrib import admin
from .models import Group, User, WishlistItem, Assignment

admin.site.register(Group)
admin.site.register(User)
admin.site.register(WishlistItem)
admin.site.register(Assignment)
