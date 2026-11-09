# AGFS Fee Scheme 18

Scheme 18 is calculator scheme ID 15. It applies to representation orders from
1 November 2026; main-hearing dates do not affect eligibility. Scheme 17 (ID 14)
ends on 31 October 2026.

All scheme 17 prices and modifiers are copied unchanged. Four new fee types are
priced for every AGFS scenario and any offence class, without modifiers:

| Code | Unit | JUNIOR | LEADJR | KC |
| --- | --- | --- | --- | --- |
| AGFS_SENT_ADD | HOUR | 48.02 | 68.94 | 91.11 |
| AGFS_MITIG | DAY | 166.00 | 266.00 | 400.00 |
| AGFS_MIT_ADD | HOUR | 48.02 | 68.94 | 91.11 |
| AGFS_BAIL_APP | DAY | 118.00 | 176.00 | 234.00 |

Amounts are GBP excluding VAT. The existing modern `JUNIOR` category covers both
junior alone and led junior. No legacy advocate categories are introduced.
Hourly quantities and rounding follow existing hourly fees, including the
existing one-unit applicability threshold. Fixed fees use `fixed_fee` and are
added once, not multiplied by the number of days.

## Data migration

No table-schema migration is required. Follow the existing fixture-driven
deployment procedure after deploying the calculator code:

```sh
pipenv run python3 manage.py migrate
pipenv run python3 manage.py cleardata
pipenv run python3 manage.py loadalldata
```

`cleardata` deletes calculator reference/pricing data. Use it only on the intended
environment, with the normal operational safeguards. The new fixture is included
in `loadalldata`; no price generation is needed during deployment.

To regenerate scheme 18 after loading all reference fixtures:

```sh
pipenv run python3 manage.py add_agfs_scheme_18
pipenv run python3 manage.py dumpprices 15 fee_calculator/apps/calculator/fixtures/price_15_agfs_18.json
```

The command uses `copyscheme` when the destination has no prices. Repeated runs
update the four new hearing fees without duplicating inherited prices. Review
and run the scheme 18 tests before deploying a regenerated fixture.

Deploy Fee Calculator before enabling these fees in CCCD. CCR integration is
outside this change.
