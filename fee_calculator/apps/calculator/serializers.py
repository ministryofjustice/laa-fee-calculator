# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import (
    Scheme, Scenario, FeeType, AdvocateType, OffenceClass, Price)


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
    fee_types = FeeTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Scenario
        fields = ('id', 'name', 'fee_types')


class AdvocateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvocateType
        fields = ('id', 'name')


class OffenceClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenceClass
        fields = ('id', 'name')


class PriceSerializer(serializers.ModelSerializer):
    scheme = SchemeSerializer(read_only=True)
    advocate_type = AdvocateTypeSerializer(read_only=True)
    fee_type = FeeTypeSerializer(read_only=True)
    offence_class = OffenceClassSerializer(read_only=True)

    class Meta:
        model = Price
        fields = ('id', 'advocate_type', 'fee_type', 'offence_class', 'scheme',
                  'amount', 'max_count')