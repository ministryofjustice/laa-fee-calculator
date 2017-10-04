# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import (
    Scheme, Scenario, FeeType, AdvocateType, OffenceClass, Price, Unit
)


class SchemeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Scheme
        fields = (
            'id',
            'effective_date',
            'start_date',
            'end_date',
            'suty_base_type',
            'description',
        )


class FeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeType
        fields = ('id', 'name', 'code', 'is_basic')


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ('id', 'name')


class AdvocateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvocateType
        fields = ('id', 'name')


class OffenceClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenceClass
        fields = ('id', 'name', 'description')


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name')


class PriceSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer(read_only=True)
    scheme = SchemeSerializer(read_only=True)
    advocate_type = AdvocateTypeSerializer(read_only=True)
    fee_type = FeeTypeSerializer(read_only=True)
    offence_class = OffenceClassSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Price
        fields = ('id', 'scenario', 'advocate_type', 'fee_type',
                  'offence_class', 'scheme', 'unit', 'fee_per_unit',
                  'uplift_percent', 'limit_from', 'limit_to',)
