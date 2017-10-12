from django.contrib import admin

from calculator.models import (
    Scheme, Scenario, FeeType, AdvocateType, OffenceClass, Unit, Price,
    Modifier, ModifierValue
)


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = (
        'description', 'suty_base_type', 'start_date', 'end_date',
    )
    list_filter = (
        'suty_base_type',
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


@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'unit',)


@admin.register(ModifierValue)
class ModifierValueAdmin(admin.ModelAdmin):
    list_display = ('modifier', 'limit_from', 'limit_to', 'modifier_percent',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'scheme', 'scenario', 'fee_type', 'advocate_type', 'offence_class',
        'fixed_fee', 'fee_per_unit', 'unit',
    )
    list_filter = (
        'scheme', 'scenario', 'fee_type', 'advocate_type', 'offence_class',
        'unit', 'modifiers',
    )
