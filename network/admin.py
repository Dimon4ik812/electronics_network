from django.contrib import admin

from .models import NetworkNode


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "city", "supplier", "debt", "created_at")
    list_filter = ("city",)
    actions = [clear_debt]
    readonly_fields = ("created_at",)


admin.site.register(NetworkNode, NetworkNodeAdmin)
