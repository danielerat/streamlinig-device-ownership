from django.contrib import admin
from stream.models import Device
# Register your models here.

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "model",
        "serial_number",
        "mac_address",
        "imei",
        "price",
        "category"
    ]
    list_per_page = 20
    list_select_related = ["owner"]
    ordering = ["name", "price", "category"]
    search_fields = [
        "name",
        "model",
        "serial_number",
        "mac_address",
        "imei",
        "owner__first_name",
        "owner__last_name",
        "owner__national_id",
        "owner__phone_number",
    ]
    list_filter = ["status", "quality", "created"]
