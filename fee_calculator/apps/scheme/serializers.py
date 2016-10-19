# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Scheme


class SchemeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Scheme
        fields = (
            'effective_date',
            'start_date',
            'end_date',
            'suty_base_type',
            'description',
        )
