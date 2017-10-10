# laa-fee-calculator
Fee calculator for LAA


Load data into calculator
==========================

```
./manage.py loaddata advocatetype feetype offenceclass price scenario scheme unit uplift
```

Calculator
==========

Swagger docs are accessible at `/api/v1/docs/`

First request `/api/v1/fee-schemes/<suty>/<order_date>/` to get the appropriate scheme.

Then request:

```
/api/v1/scenarios/?scheme=<scheme_id>
/api/v1/offence-classes/?scheme=<scheme_id>
/api/v1/advocate-types/?scheme=<scheme_id>
```

to get the options for these values.

Once all of these choices have been made, use the values to request:

```
/api/v1/fee-types/?scheme=<scheme_id>&scenario=<scenario_id>&advocate_typ=<advocate_type_id>&offence_class=<offence_class_id>
```

This will give you a list of fee types which are applicable for the situation, along with the units of each fee type and the units of any possibly applicable uplifts.

For each applicable fee type and unit, make a request to the calculate endpoint:

```
/api/v1/calculate/?scheme=<scheme_id>&scenario=<scenario_id>&advocate_type=<advocate_type_id>&offence_class=<offence_class_id>&fee_type_code=<fee_type_code>&unit=<unit_id>&unit_count=<number_of_units>
```

For uplifts, add additional URL parameters of the form:

```
uplift_unit_%n=<unit_id>&uplift_unit_count_%n=<number_of_units>
```

where %n is an integer (>=1) which matches for each uplift e.g. if there are 3 defendants and 2 cases one would add:

```
&uplift_unit_1=DEFENDANT&uplift_unit_count_1=3&uplift_unit_2=CASE&uplift_unit_count_2=2
```

to the calculate request.

This should then return a response of the form:

```
{'amount': '134.00'}
```

which is the total price for that fee, taking into account differing prices for different counts and all uplifts.

For example when calculating the basic advocate's fee, if the number of days attended is 45, under Scheme 9 the returned amount will include the fixed fee for the first 2 days, the daily fee for days 3-40 and the reduced daily fee for days 41-45.

Prices
======

As well as the calculator endpoint, one can also get a list of prices directly from the endpoint `/api/v1/prices/`. See swagger documentation for available filters.
