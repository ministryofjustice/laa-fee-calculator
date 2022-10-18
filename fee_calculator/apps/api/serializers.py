# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from calculator.models import (
    Scheme, Scenario, FeeType, AdvocateType, OffenceClass, Price, Unit,
    ModifierType, Modifier, ScenarioCode
)


class SchemeListQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        help_text="Graduated fee scheme type",
        choices=('AGFS', 'LGFS'),
        required=False
    )
    case_date = serializers.CharField(
        help_text="Representation order date for which you would like a list of applicable fee schemes",
        required=False
    )

    main_hearing_date = serializers.CharField(
        help_text="Main hearing date for which you would like a list of applicable fee schemes",
        required=False
    )


class BasePriceFilteredQuerySerializer(serializers.Serializer):
    scenario = serializers.IntegerField(
        help_text='',
        required=False,
    )
    advocate_type = serializers.CharField(
        help_text='Note the query will return prices with `advocate_type_id` either matching the value or null.',
        required=False,
    )
    offence_class = serializers.CharField(
        help_text='Note the query will return prices with `offence_class_id` either matching the value or null.',
        required=False,
    )
    fee_type_code = serializers.CharField(
        help_text='',
        required=False,
    )


class CalculatorQuerySerializer(serializers.Serializer):
    class UnitField(serializers.DecimalField):
        def __init__(self, name, **kwargs):
            new_kwargs = {'help_text': f'Quantity of the price unit: {name}',
                          'required': False,
                          'max_digits': 100,
                          'decimal_places': 5}
            new_kwargs.update(kwargs)
            super().__init__(**new_kwargs)

    class ModifierTypeField(serializers.DecimalField):
        def __init__(self, description, **kwargs):
            new_kwargs = {'help_text': f'Price modifier: {description}',
                          'required': False,
                          'max_digits': 100,
                          'decimal_places': 5}
            new_kwargs.update(kwargs)
            super().__init__(**new_kwargs)

    scenario = serializers.IntegerField(
        help_text='',
        required=True,
    )
    fee_type_code = serializers.CharField(
        help_text='',
        required=True,
    )
    advocate_type = serializers.CharField(
        help_text='Note the query will return prices with `advocate_type_id` either matching the value or null.',
        required=False,
    )
    offence_class = serializers.CharField(
        help_text='Note the query will return prices with `offence_class_id` either matching the value or null.',
        required=False,
    )
    case = UnitField('Case')
    day = UnitField('Whole Days')
    defendant = UnitField('Defendants')
    fixed = UnitField('Fixed Amount')
    halfday = UnitField('Half Days')
    hour = UnitField('Hours')
    month = UnitField('Months')
    ppe = UnitField('Pages of Prosecuting Evidence')
    pw = UnitField('Prosecution Witnesses')
    third = UnitField('Third of a trial')
    level = UnitField('Evidence provision fee level')
    number_of_cases = ModifierTypeField('Number of cases')
    number_of_defendants = ModifierTypeField('Number of defendants')
    number_of_hearings = ModifierTypeField('Number of hearings')
    trial_length = ModifierTypeField('Trial length')
    pages_of_prosecuting_evidence = ModifierTypeField('Pages of prosecuting evidence')
    retrial_interval = ModifierTypeField('Whole months between trials')
    third_cracked = ModifierTypeField('Third in which a trial cracked')
    warrant_interval = ModifierTypeField('Whole months between warrant issue and execution')


class CalculatorResponseSerializer(serializers.Serializer):
    serializers.DecimalField(max_digits=None, decimal_places=2)


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

    def get_code(self, obj) -> str:
        if hasattr(self, 'scheme'):
            try:
                return obj.codes.get(scheme_type=self.scheme.base_type).code
            except ScenarioCode.DoesNotExist:
                pass
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
