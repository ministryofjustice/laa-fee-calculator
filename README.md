# laa-fee-calculator
Fee calculator for LAA use

[![CircleCI](https://circleci.com/gh/ministryofjustice/laa-fee-calculator/tree/main.svg?style=svg)](https://circleci.com/gh/ministryofjustice/laa-fee-calculator/tree/main)
[![Known Vulnerabilities](https://snyk.io/test/github/ministryofjustice/laa-fee-calculator/badge.svg)](https://snyk.io/test/github/ministryofjustice/laa-fee-calculator)
[![Ministry of Justice Repository Compliance Badge](https://github-community.service.justice.gov.uk/repository-standards/api/laa-fee-calculator/badge)](https://github-community.service.justice.gov.uk/repository-standards/laa-fee-calculator)

For development setup see instructions [here](./docs/DEVELOPMENT.md)

## Load data into calculator

```
./manage.py migrate
./manage.py cleardata
./manage.py loadalldata
```

## Calculator


Swagger docs are accessible at `/api/v1/docs/`

First request `/api/v1/fee-schemes/?type=<type>&case_date=<representation_order_date>&main_hearing_date=<main_hearing_date>` to get the appropriate scheme.

Then request:

```curl
/api/v1/fee-schemes/<scheme_id>/scenarios/
/api/v1/fee-schemes/<scheme_id>/offence-classes/
/api/v1/fee-schemes/<scheme_id>/advocate-types/
```

to get the options for these values.

Once all of these choices have been made, use the values to request:

```curl
/api/v1/fee-schemes/<scheme_id>/fee-types/?scenario=<scenario_id>&advocate_typ=<advocate_type_id>&offence_class=<offence_class_id>
```

This will give you a list of fee types which are applicable for the situation

For each applicable fee type, find out the information required by the user
by requesting the relevant units and modifiers:

```curl
/api/v1/fee-schemes/<scheme_id>/units/?scenario=<scenario_id>&advocate_typ=<advocate_type_id>&offence_class=<offence_class_id>&fee_type_code=<fee_type_code>
/api/v1/fee-schemes/<scheme_id>/modifiers/?scenario=<scenario_id>&advocate_typ=<advocate_type_id>&offence_class=<offence_class_id>&fee_type_code=<fee_type_code>
```

Make a request to the calculate endpoint as shown:

```curl
/api/v1/fee-schemes/<scheme_id>/calculate/?scenario=<scenario_id>&advocate_type=<advocate_type_id>&offence_class=<offence_class_id>&fee_type_code=<fee_type_code>&<unit_id>=<number_of_units>
```

With a `<unit_id>=<number_of_units>` for each applicable unit of the fee type eg for the basic fee of a trial that was 6 days long with 1002 pages of evidence and 2 witnesses one would add:

```curl
&day=6&ppe=102&pw=2
```

For modifiers, for every request to the calculate endpoint, add additional URL parameters of the form `<modifier_type_name>=<number_of_units>` eg if there are 3 defendants and 2 cases one would add:

```curl
&number_of_defendants=3&number_of_cases=2
```

to the calculate request.

This should then return a response of the form:

```json
{"amount": "134.00"}
```

which is the total price for that fee, taking into account differing prices for different counts and all modifiers.

For example when calculating the basic advocate's fee, if the number of days attended is 45, under Scheme 9 the returned amount will include the fixed fee for the first 2 days, the daily fee for days 3-40 and the reduced daily fee for days 41-45.

## Prices


As well as the calculator endpoint, one can also get a list of prices directly from the endpoint `/api/v1/fee-schemes/<scheme_id>/prices/`. See swagger documentation for available filters.

## Deployment

Currently a commit to main will kickoff circle CI pipeline for deployment to available enviroments

* To check what is the status of the application pods:

```bash
kubectl get pods -n laa-fee-calculator-production
NAME                                  READY   STATUS    RESTARTS   AGE
laa-fee-calculator-554fb6595d-97979   1/1     Running   0          5h53m
laa-fee-calculator-554fb6595d-kmxc8   1/1     Running   0          5h53m
laa-fee-calculator-554fb6595d-xs2v9   1/1     Running   0          5h53m
```

## New fee schemes

To generate a new fee scheme:

* add fee scheme fixture to `fee_calculator/apps/calculator/fixtures/scheme.json`.

  Set `end_date` of the previous fee scheme of the same `base_type` and the `start_date` of the new scheme, so that they are contiguous. Increment the `pk` and set the other attributes of the new scheme.

  ```json
  {
    "model": "calculator.scheme",
    "pk": 15,
    "fields": {
      "start_date": "2027-01-01",
      "end_date": null,
      "base_type": 1,
      "description": "AGFS Fee Scheme 18"
    }
  }
  ```

* apply the new fee scheme:

  ```bash
  ./manage.py cleardata
  ./manage.py loadalldata
  ```

* use management tools to copy a previous scheme's prices:

  ```bash
  ./manage.py copyscheme 14 15
  ```

- dump the updated prices back to the new scheme's fixture file. Price fixtures are stored per scheme in `fee_calculator/apps/calculator/fixtures/` with the naming convention `price_<nn>_<type>_<version>.json`.

  ```bash
  ./manage.py dumpprices 15 fee_calculator/apps/calculator/fixtures/price_15_agfs_18.json
  ```

* add the new price fixture filename to `fee_calculator/apps/calculator/management/commands/loadalldata.py`.

* edit the new price fixture file to adjust prices as needed for the new scheme.

* apply the new price data:

  ```bash
  ./manage.py cleardata
  ./manage.py loadalldata
  ```

## New fee types

To add a new fee type to a scheme:

- amend `fee_calculator/apps/calculator/fixtures/feetype.json` to add the new fee type:

  ```json
    ...
    },
    {
      "model": "calculator.feetype",
      "pk": 234,
      "fields": {
        "name": "New fee type",
        "code": "NEW_FEE_CODE",
        "is_basic": false,
        "aggregation": "sum"
      }
    }
  ```

- clear and load data:

  ```bash
  ./manage.py cleardata
  ./manage.py loadalldata
  ```

- create prices in the database for the new fee type by copying another fee type's, if appropriate:

  ```bash
  ./manage.py copyfeetype 233 14 234 15
  ```

  This will copy the values of fee_type id 233 in scheme id 14 to fee_type id 234 in scheme id 15 in the database. Run `./manage.py copyfeetype -h` for details of the command.

- dump the updated prices back to the relevant scheme's fixture file:

  ```bash
  ./manage.py dumpprices 15 fee_calculator/apps/calculator/fixtures/price_15_agfs_18.json
  ```
