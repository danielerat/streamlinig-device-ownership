
from django.utils.html import format_html, urlencode
from django.contrib import admin
from stream.models import Device, DeviceImage, Warranty
# Register your models here.


class DeviceImageInline(admin.TabularInline):
    model = DeviceImage
    readonly_fields = ['thumbnail']
    min_num = 2
    max_num = 10
    extra = 0

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')

    class Media:

        css = {
            'all': ['stream/styles.css']
        }


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
    inlines = [DeviceImageInline]


admin.site.register(Warranty)
