# laa-fee-calculator
Fee calculator for LAA


Load data into calculator
==========================

```
./manage.py loaddata advocatetype feetype offenceclass price scenario scheme unit modifier modifiervalue
```

Calculator
==========

Swagger docs are accessible at `/api/v1/docs/`

First request `/api/v1/fee-schemes/?supplier_type=<supplier_type>&case_date=<case_date>` to get the appropriate scheme.

Then request:

```
/api/v1/fee-schemes/<scheme_id>/scenarios/
/api/v1/fee-schemes/<scheme_id>/offence-classes/
/api/v1/fee-schemes/<scheme_id>/advocate-types/
```

to get the options for these values.

Once all of these choices have been made, use the values to request:

```
/api/v1/fee-schemes/<scheme_id>/fee-types/?scenario=<scenario_id>&advocate_typ=<advocate_type_id>&offence_class=<offence_class_id>
```

This will give you a list of fee types which are applicable for the situation

For each applicable fee type, find out the information required by the user
by requesting the relevant units and modifiers:

```
/api/v1/fee-schemes/<scheme_id>/units/?scenario=<scenario_id>&advocate_typ=<advocate_type_id>&offence_class=<offence_class_id>&fee_type_code=<fee_type_code>
/api/v1/fee-schemes/<scheme_id>/modifiers/?scenario=<scenario_id>&advocate_typ=<advocate_type_id>&offence_class=<offence_class_id>&fee_type_code=<fee_type_code>
```

For each applicable unit, make a request to the calculate endpoint as shown:

```
/api/v1/fee-schemes/<scheme_id>/calculate/?scenario=<scenario_id>&advocate_type=<advocate_type_id>&offence_class=<offence_class_id>&fee_type_code=<fee_type_code>&unit=<unit_id>&unit_count=<number_of_units>
```

For modifiers, for every request to the calculate endpoint, add additional URL parameters of the form:

```
modifier_%n=<number_of_units>
```

where %n is an integer which is the id of the relevant modifier eg if there are 3 defendants and 2 cases one would add:

```
&modifier_2=3&modifier_1=2
```

to the calculate request.

This should then return a response of the form:

```
{'amount': '134.00'}
```

which is the total price for that fee, taking into account differing prices for different counts and all modifiers.

For example when calculating the basic advocate's fee, if the number of days attended is 45, under Scheme 9 the returned amount will include the fixed fee for the first 2 days, the daily fee for days 3-40 and the reduced daily fee for days 41-45.

Prices
======

As well as the calculator endpoint, one can also get a list of prices directly from the endpoint `/api/v1/fee-schemes/<scheme_id>/prices/`. See swagger documentation for available filters.
