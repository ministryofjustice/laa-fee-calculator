# laa-fee-calculator
Fee calculator for LAA

For development setup see instructions [here](./docs/DEVELOPMENT.md)

## Load data into calculator

```
./manage.py migrate
./manage.py cleardata
./manage.py loadalldata
```

## Calculator


Swagger docs are accessible at `/api/v1/docs/`

First request `/api/v1/fee-schemes/?type=<type>&case_date=<case_date>` to get the appropriate scheme.

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

Currently a commit to master will kickoff circle CI pipeline for deployment to available enviroments

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

  Set `end_date` of the previous fee scheme of the same `base_type` and the `start_date` of the new scheme, so that they are contiguous. increment the `pk` and set the other attributes of the new scheme.

  ```json
  {
    "model": "calculator.scheme",
    "pk": 5,
    "fields": {
      "start_date": "2020-07-02",
      "end_date": null,
      "base_type": 1,
      "description": "AGFS Fee Scheme 12"
  }
  ```

* apply the new fee scheme

  ```bash
  ./manage.py cleardata
  ./manage.py loadalldata
  ```

* use management tools to copy previous scheme prices

  ```bash
  ./manage.py copyscheme 4 5
  ```

* use standard django `dumpdata` to collect the all the prices as a fixture.

  You should pretty format the json output afterwards. You might want to dump to a separate file to do a diff first, to check changes made.

  ```bash
  ./manage.py dumpdata calculator.price --indent 2 > fee_calculator/apps/calculator/fixtures/price.json
  ```

## New fee types

To add a new fee type to a scheme:

- amend `fee_calculator/apps/calculator/fixtures/feetype.json`

  ```json
    ...
    },
    {
      "model": "calculator.feetype",
      "pk": 229,
      "fields": {
        "name": "Paper heavy case",
        "code": "AGFS_PAP_HEAVY",
        "is_basic": false,
        "aggregation": "sum"
      }
    }
  ```

- clear and load data

  ```bash
  ./manage.py cleardata
  ./manage.py loadalldata
  ```

- create prices for the new fee type by copying another another fee type's, if appropriate

  ```bash
  ./manage.py copyfeetype 29 229 5
  ```

  call `./manage.py copyfeetype -h` for details on the command

- recreate fixtures for the new prices

  ```bash
  ./manage.py dumpdata calculator.price --indent 2 > fee_calculator/apps/calculator/fixtures/price.json
  ```
