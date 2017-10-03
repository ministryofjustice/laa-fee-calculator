from django.contrib import admin

from calculator.models import (
    Scheme, Scenario, FeeType, AdvocateType, OffenceClass, Unit, Price
)


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = (
        'description', 'suty_base_type', 'effective_date',
        'start_date', 'end_date',
    )


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_basic')


@admin.register(AdvocateType)
class AdvocateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


@admin.register(OffenceClass)
class OffenceClassAdmin(admin.ModelAdmin):
    list_display = ('description', 'id', 'name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'scheme', 'scenario', 'fee_type', 'advocate_type', 'offence_class',
        'fee_per_unit', 'unit',
    )
