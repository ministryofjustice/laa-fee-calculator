# -*- coding: utf-8 -*-
from extended_choices import Choices


SUPPLIER_BASE_TYPE = Choices(
    ('ADVOCATE', 1, 'Advocate'),
    ('SOLICITOR', 2, 'Solicitor'),
)


AGGREGATION_TYPE = Choices(
    ('SUM', 'sum', 'Sum'),
    ('MAX', 'max', 'Max')
)
