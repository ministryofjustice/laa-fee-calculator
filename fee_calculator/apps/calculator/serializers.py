# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import (
    Scheme, Scenario, FeeType, AdvocateType, OffenceClass, Price, Unit,
    ModifierType, Modifier
)


class SchemeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Scheme
        fields = (
            'id',
            'start_date',
            'end_date',
            'type',
            'description',
        )


class FeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeType
        fields = (
            'id',
            'name',
            'code',
            'is_basic',
            'aggregation',
        )


class ScenarioSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'scheme_pk' in self.context:
            self.scheme = get_object_or_404(Scheme, pk=self.context['scheme_pk'])

    class Meta:
        model = Scenario
        fields = (
            'id',
            'name',
            'code',
        )

    def get_code(self, obj):
        if hasattr(self, 'scheme'):
            return obj.codes.get(scheme_type=self.scheme.base_type).code
        return None


class AdvocateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvocateType
        fields = (
            'id',
            'name',
        )


class OffenceClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenceClass
        fields = (
            'id',
            'name',
            'description',
        )


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = (
            'id',
            'name',
        )


class ModifierTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierType
        fields = (
            'id',
            'name',
            'description',
            'unit',
        )


class ModifierSerializer(serializers.ModelSerializer):
    modifier_type = ModifierTypeSerializer(read_only=True)

    class Meta:
        model = Modifier
        fields = (
            'limit_from',
            'limit_to',
            'fixed_percent',
            'percent_per_unit',
            'modifier_type',
            'required',
            'priority',
            'strict_range',
        )


class PriceSerializer(serializers.ModelSerializer):
    modifiers = ModifierSerializer(many=True, read_only=True)

    class Meta:
        model = Price
        fields = (
            'id',
            'scenario',
            'advocate_type',
            'fee_type',
            'offence_class',
            'scheme',
            'unit',
            'fee_per_unit',
            'fixed_fee',
            'limit_from',
            'limit_to',
            'modifiers',
            'strict_range',
        )
