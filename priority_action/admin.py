from django.contrib import admin
from .models import (
    Intent,
    IntentChange,
    Correlation,
    CorrelationChange,
    Sales,
    SalesChange,
    Period,
)


@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    pass


@admin.register(IntentChange)
class IntentChange(admin.ModelAdmin):
    pass


@admin.register(Correlation)
class CorrelationAdmin(admin.ModelAdmin):
    pass


@admin.register(CorrelationChange)
class CorrelationChangeAdmin(admin.ModelAdmin):
    pass


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    pass


@admin.register(SalesChange)
class SalesChangeAdmin(admin.ModelAdmin):
    pass


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    pass