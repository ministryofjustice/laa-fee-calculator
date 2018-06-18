# -*- coding: utf-8 -*-
from extended_choices import Choices


SCHEME_TYPE = Choices(
    ('AGFS', 1, 'Advocate Graduated Fee Scheme'),
    ('LGFS', 2, 'Litigator Graduated Fee Scheme'),
)


AGGREGATION_TYPE = Choices(
    ('SUM', 'sum', 'Sum'),
    ('MAX', 'max', 'Max')
)
