# -*- coding: utf-8 -*-
from extended_choices import Choices


SUTY_BASE_TYPE = Choices(
    ('ADVOCATE', 1, 'Advocate'),
    ('SOLICITOR', 2, 'Solicitor'),
)


APRT_APPROVAL_TYPE = Choices(
    ('MANUAL', 1, 'Manual'),
    ('VALIDATE', 2, 'Validate'),
)


HEARING_TYPE = Choices(
    ('ANCILLARY', 1, 'Ancillary'),
    ('MAIN', 2, 'Main'),
)
