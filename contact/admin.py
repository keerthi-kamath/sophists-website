from django.contrib import admin
from .models import Contact, Events


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "timestamp")


@admin.register(Events)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "date_and_time")
