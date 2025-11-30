from django.contrib import admin
from .models import User, WishlistItem, Assignment
from .views import generate_assignments


@admin.action(description="Generate Secret Santa Assignments")
def generate_assignments_action(modeladmin, request, queryset):
    generate_assignments()
    admin_message = "🎅 Assignments generated successfully! Check the Assignments table."
    modeladmin.message_user(request, admin_message)


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [generate_assignments_action]


admin.site.register(User, UserAdmin)
admin.site.register(WishlistItem)
admin.site.register(Assignment)
