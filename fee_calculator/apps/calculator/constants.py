# -*- coding: utf-8 -*-
from django.db import models


class SchemeType(models.IntegerChoices):
    AGFS = 1, 'Advocate Graduated Fee Scheme'
    LGFS = 2, 'Litigator Graduated Fee Scheme'


class AggregationType(models.TextChoices):
    SUM = 'sum', 'Sum'
    MAX = 'max', 'Max'
