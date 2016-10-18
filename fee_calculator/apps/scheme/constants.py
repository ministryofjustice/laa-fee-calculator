# -*- coding: utf-8 -*-
from extended_choices import Choices


SUTY_BASE_TYPE = Choices(
    ('ADVOCATE',  1, 'Advocate'),
    ('SOLICITOR',   2, 'Solicitor'),
)


PSTY_PERSON_TYPE = Choices(
    ('JRALONE', 1, 'JRALONE'),
    ('LEDJR', 2, 'LEDJR'),
    ('LEADJR', 3, 'LEADJR'),
    ('QC', 4, 'QC'),
)


FEE_UNIT = Choices(
    ('HOUR', 1, 'Hour'),
    ('HALF_DAY', 2, 'Half day'),
    ('DAY', 3, 'Day'),
    ('CASE', 4, 'Case'),
    ('FIXED', 5, 'Fixed'),
)


APRT_APPROVAL_TYPE = Choices(
    ('MANUAL',  1, 'Manual'),
    ('VALIDATE',   2, 'Validate'),
)


HEARING_TYPE = Choices(
    ('ANCILLARY',  1, 'Ancillary'),
    ('MAIN',   2, 'Main'),
)
