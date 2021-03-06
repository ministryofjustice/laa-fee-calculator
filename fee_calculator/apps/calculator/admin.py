from django.contrib import admin

from calculator.models import (
    Scheme, Scenario, FeeType, AdvocateType, OffenceClass, Unit, Price,
    ModifierType, Modifier, ScenarioCode
)


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = (
        'description', 'base_type', 'start_date', 'end_date',
    )
    list_filter = (
        'base_type',
    )


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ScenarioCode)
class ScenarioCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'scenario', 'scheme_type',)


@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_basic',)


@admin.register(AdvocateType)
class AdvocateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


@admin.register(OffenceClass)
class OffenceClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


@admin.register(ModifierType)
class ModifierTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'unit',)


@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    list_display = ('modifier_type', 'limit_from', 'limit_to', 'percent_per_unit',)


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
