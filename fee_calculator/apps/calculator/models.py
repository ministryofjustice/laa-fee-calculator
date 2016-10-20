# -*- coding: utf-8 -*-
from django.db import models

from .constants import (SUTY_BASE_TYPE, PSTY_PERSON_TYPE, FEE_UNIT,
                        APRT_APPROVAL_TYPE, HEARING_TYPE)


class Scheme(models.Model):
    effective_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    suty_base_type = models.PositiveSmallIntegerField(choices=SUTY_BASE_TYPE)
    description = models.CharField(max_length=150)


class BillType(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    enabled = models.BooleanField()
    appeal_allowed = models.BooleanField()
    auto_authorise_threshold = models.PositiveSmallIntegerField(null=True)
    auto_authorise_threshold_num = models.PositiveSmallIntegerField(null=True)
    final_bill = models.BooleanField()
    ordering_value = models.PositiveSmallIntegerField()
    recoup_allowed = models.BooleanField()
    vat = models.BooleanField()


class BillSubType(models.Model):
    cccd_fee_type = models.CharField(max_length=10, null=True)
    bill_type = models.ForeignKey('BillType', related_name='sub_types')
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    calculation_method = models.PositiveSmallIntegerField()  # TODO need to sort choices for this
    case_uplift_allowed = models.NullBooleanField()
    aprt_approval_type = models.PositiveSmallIntegerField(
        choices=APRT_APPROVAL_TYPE)
    cis_transaction_category = models.PositiveSmallIntegerField()  # TODO need to sort choices or foreign key for this
    defendant_uplift_allowed = models.BooleanField()
    enabled = models.BooleanField()
    evid_threshold_amount = models.PositiveSmallIntegerField(null=True)
    hearing_type = models.PositiveSmallIntegerField(
        null=True, choices=HEARING_TYPE)
    max_claim_value = models.PositiveIntegerField()
    notes = models.TextField(null=True)
    on_indictment = models.NullBooleanField()
    prior_auth_reqd = models.NullBooleanField()
    rate_applicable = models.BooleanField()
    refference_prefix = models.CharField(max_length=10, null=True)


class Fee(models.Model):
    scheme = models.ForeignKey('Scheme', related_name='fees')
    psty_person_type = models.PositiveSmallIntegerField(
        choices=PSTY_PERSON_TYPE)
    limit_from = models.PositiveSmallIntegerField()
    limit_to = models.PositiveSmallIntegerField(null=True)
    fee_per_unit = models.PositiveSmallIntegerField()
    unit = models.PositiveSmallIntegerField(choices=FEE_UNIT)
    additional_uplift_perc = models.PositiveSmallIntegerField()
    bist_bill_sub_type = models.ForeignKey('BillSubType', related_name='fees')
