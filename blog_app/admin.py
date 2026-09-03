from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog_app.models import Article, UserProfile


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "word_count", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("created_at",)
    readonly_fields = ("word_count", "created_at", "updated_at")


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Persmissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Imporant Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {  # "FieldTitle"
                "classes": ("wide",),  # "collapse"
                "fields": ("email", "password1"),
            },
        ),
    )
    list_display = ("email", "username", "is_staff", "is_active")
    ordering = ("email",)
    # search_fields = ("email",)


admin.site.register(Article, ArticleAdmin)
admin.site.register(UserProfile, CustomUserAdmin)
