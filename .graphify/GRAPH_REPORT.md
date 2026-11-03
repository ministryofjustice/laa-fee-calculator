# Graph Report - .  (2026-09-08)

## Corpus Check
- Corpus is ~40,595 words - fits in a single context window. You may not need a graph.

## Summary
- 1351 nodes · 3228 edges · 136 communities detected
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 991 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 973 · method: 658 · calls: 428 · ON_BRANCH: 400 · contains: 281 · PARENT_OF: 264 · inherits: 114 · imports_from: 42 · rationale_for: 39 · semantically_similar_to: 12 · MODIFIES: 11 · conceptually_related_to: 6


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 186 · Candidates: 261
- Excluded: 276 untracked · 0 ignored · 0 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `b03c3f3`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `Scheme` - 81 edges
2. `Price` - 80 edges
3. `FeeType` - 70 edges
4. `Scenario` - 68 edges
5. `OffenceClass` - 68 edges
6. `AdvocateType` - 58 edges
7. `Unit` - 54 edges
8. `ModifierType` - 50 edges
9. `DatePicker` - 40 edges
10. `Modifier` - 37 edges

## Surprising Connections (you probably didn't know these)
- `Generate a presenter for the price` --uses--> `DelegatorMixin`  [INFERRED]
  fee_calculator/apps/viewer/presenters/price_presenters.py → fee_calculator/apps/viewer/presenters/helpers.py
- `Command` --uses--> `Price`  [INFERRED]
  fee_calculator/apps/calculator/management/commands/agfs_2022_uplift.py → fee_calculator/apps/calculator/models.py
- `Command` --uses--> `Scheme`  [INFERRED]
  fee_calculator/apps/calculator/management/commands/agfs_2022_uplift.py → fee_calculator/apps/calculator/models.py
- `Command` --uses--> `Price`  [INFERRED]
  fee_calculator/apps/calculator/management/commands/copyscheme.py → fee_calculator/apps/calculator/models.py
- `Command` --uses--> `Scheme`  [INFERRED]
  fee_calculator/apps/calculator/management/commands/copyscheme.py → fee_calculator/apps/calculator/models.py

## Hyperedges (group relationships)
- **Fee Scheme View Composition** — viewer_fee_scheme_page, viewer_fee_scheme_summary, viewer_fee_scheme_filter_form, viewer_prices_table, viewer_prices_cards, viewer_offence_classes_table, viewer_scheme_scenarios_table [EXTRACTED 1.00]
- **Development Kubernetes Application Stack** — kubernetes_dev_deployment, kubernetes_dev_service, kubernetes_dev_ingress [INFERRED 0.90]
- **Production Kubernetes Application Stack** — kubernetes_production_deployment, kubernetes_production_service, kubernetes_production_ingress [INFERRED 0.90]
- **Staging Kubernetes Application Stack** — kubernetes_staging_deployment, kubernetes_staging_service, kubernetes_staging_ingress [INFERRED 0.90]
- **GOV.UK Visual Identity Assets** — govuk_icon_180_png, govuk_icon_192_png, govuk_icon_512_png, govuk_icon_mask_svg, govuk_opengraph_image_png, moj_govuk_logotype_crown_png [INFERRED 0.94]
- **MOJ Alert Status Symbols** — moj_icon_alert_information_svg, moj_icon_alert_success_svg, moj_icon_alert_warning_svg [INFERRED 0.90]
- **MOJ Directional Arrow Variants** — moj_icon_arrow_black_down_svg, moj_icon_arrow_black_up_svg, moj_icon_arrow_white_down_svg, moj_icon_arrow_white_up_svg [INFERRED 0.96]
- **WYSIWYG Formatting Controls** — icon_wysiwyg_bold, icon_wysiwyg_italic, icon_wysiwyg_ordered_list, icon_wysiwyg_underline, icon_wysiwyg_unordered_list [EXTRACTED 1.00]
- **MOJ Apple Touch Icon Size Set (2024)** — moj_apple_touch_icon_152x152_2024, moj_apple_touch_icon_167x167_2024, moj_apple_touch_icon_180x180_2024, moj_apple_touch_icon_2024 [EXTRACTED 1.00]
- **MOJ Crest Brand Assets (2024)** — moj_logotype_crest_2024_png, moj_logotype_crest_2024_svg, moj_opengraph_image_2024 [INFERRED 0.90]

## Communities

### Community 0 - "Fee Calculator Data Models"
Cohesion: 0.10
Nodes (81): ModelOrNoneChoiceFilter, FeeTypeFilter, Meta, PriceFilter, SchemeFilter, SchemeListQuerySerializer, BasePriceFilteredQuerySerializer, CalculatorQuerySerializer (+73 more)

### Community 68 - "Preloaded Database Test Runner"
Cohesion: 0.40
Nodes (3): PreloadDataDiscoverRunner, XMLTestRunner, Run the unit tests for all the test labels in the provided list.          Test l

### Community 69 - "Advocate Type API Tests"
Cohesion: 0.33
Nodes (1): AdvocateTypeApiTestCase

### Community 65 - "Price API Tests"
Cohesion: 0.33
Nodes (2): APITestCase, PriceApiTestCase

### Community 56 - "Fee Type API Tests"
Cohesion: 0.22
Nodes (1): FeeTypeApiTestCase

### Community 21 - "Scheme Filter Tests"
Cohesion: 0.13
Nodes (1): SchemeFilterTestCase

### Community 41 - "Viewer Page Tests"
Cohesion: 0.21
Nodes (5): TestCase, IndexTestCase, FeeSchemesTestCase, FeeSchemeTestCase, ScenariosTestCase

### Community 51 - "Modifier Type API Tests"
Cohesion: 0.20
Nodes (1): ModifierTypeApiTestCase

### Community 70 - "Offence Class API Tests"
Cohesion: 0.33
Nodes (1): OffenceClassApiTestCase

### Community 71 - "Scenario API Tests"
Cohesion: 0.33
Nodes (1): ScenarioApiTestCase

### Community 13 - "Recent Scheme Dependency Updates"
Cohesion: 0.15
Nodes (18): 11e8a1c Bump coverage from 7.15.0 to 7.15.2, 253f8c4 Add AGFS 17 tests, 2d599ce CTSKF-1766 Set actual start date of AGFS scheme 17, 3a9de6d Merge pull request #713 from ministryofjustice/dependabot/pip/sentry-sdk-2.65.0, 430721d Merge pull request #711 from ministryofjustice/dependabot/pip/drf-spectacular-0.30.0, 484ffb3 Merge pull request #715 from ministryofjustice/dependabot/pip/coverage-7.15.2, 7f90a0e Bump django from 6.0.6 to 6.0.7, 91611b3 Merge pull request #703 from ministryofjustice/ctskf-1760-agfs-17 (+10 more)

### Community 15 - "Scheme API Tests"
Cohesion: 0.11
Nodes (1): SchemeApiTestCase

### Community 52 - "Unit API Tests"
Cohesion: 0.20
Nodes (1): UnitApiTestCase

### Community 34 - "Advocate Category Compatibility"
Cohesion: 0.26
Nodes (1): FixAdvocateCategoryTestCase

### Community 3 - "Fee Uplift Commands"
Cohesion: 0.06
Nodes (19): fee_code_for(), basic_fixed_fee_for(), fixed_and_misc_fee_for(), check_uplift(), Command, BaseCommand, Command, Command (+11 more)

### Community 35 - "Price Fixture Management"
Cohesion: 0.26
Nodes (10): 00b2479 Bump actions/checkout from 7.0.0 to 7.0.1, 10760d5 Merge pull request #719 from ministryofjustice/dependabot/pip/sentry-sdk-2.66.1, 2a76ce4 Merge pull request #718 from ministryofjustice/dependabot/github_actions/actions/checkout-7.0.1, 47268ac Bump github/codeql-action/upload-sarif from 4.37.3 to 4.37.4, 4f1319e Break price.json into smaller files, 51cad34 Merge pull request #720 from ministryofjustice/dependabot/github_actions/github/codeql-action/upload-sarif-4.37.3, 620bebd Merge pull request #717 from ministryofjustice/mw/refactor-prices, 71b1b55 Merge pull request #721 from ministryofjustice/dependabot/github_actions/github/codeql-action/upload-sarif-4.37.4 (+2 more)

### Community 57 - "Fee Generation Command"
Cohesion: 0.39
Nodes (5): generate_lgfs_fees(), generate_evidence_provision_fees(), generate_lgfs_warrant_fees(), generate_agfs10_fees(), generate_agfs_10_warrant_fees()

### Community 72 - "Bulk Fixture Loading"
Cohesion: 0.40
Nodes (3): Command, LoadDataCommand, Loads fixtures files for a given label. This method is largely copied         fr

### Community 84 - "Migration 0001 Initial Schema"
Cohesion: 1.00
Nodes (1): Migration

### Community 85 - "Migration 0002 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 86 - "Migration 0003 Scenario Cleanup"
Cohesion: 1.00
Nodes (1): Migration

### Community 87 - "Migration 0004 Price Cleanup"
Cohesion: 1.00
Nodes (1): Migration

### Community 88 - "Migration 0005 Fixed Fees"
Cohesion: 1.00
Nodes (1): Migration

### Community 89 - "Migration 0006 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 90 - "Migration 0007 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 91 - "Migration 0008 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 92 - "Migration 0009 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 93 - "Migration 0010 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 94 - "Migration 0011 Scheme Dates"
Cohesion: 1.00
Nodes (1): Migration

### Community 95 - "Migration 0012 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 96 - "Migration 0013 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 97 - "Migration 0014 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 98 - "Migration 0015 Required Modifiers"
Cohesion: 1.00
Nodes (1): Migration

### Community 99 - "Migration 0016 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 100 - "Migration 0017 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 101 - "Migration 0018 Strict Modifiers"
Cohesion: 1.00
Nodes (1): Migration

### Community 102 - "Migration 0019 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 103 - "Migration 0020 Fee Aggregation"
Cohesion: 1.00
Nodes (1): Migration

### Community 104 - "Migration 0021 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 105 - "Migration 0022 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 106 - "Migration 0023 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 107 - "Migration 0024 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 108 - "Migration 0025 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 109 - "Migration 0026 Strict Prices"
Cohesion: 1.00
Nodes (1): Migration

### Community 110 - "Migration 0027 Model Updates"
Cohesion: 1.00
Nodes (1): Migration

### Community 111 - "Migration 0028 Hearing Dates"
Cohesion: 1.00
Nodes (1): Migration

### Community 1 - "Calculator Fee Test Framework"
Cohesion: 0.05
Nodes (35): CalculatorTestCase, SimpleTestCase, AgfsCalculatorTestCase, FeeTypeUnitMixin, LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, BaseWarrantFeeTestMixin, Agfs10PlusWarrantFeeTestMixin (+27 more)

### Community 53 - "API Test Utilities"
Cohesion: 0.22
Nodes (4): bill_to_code(), prevent_request_warnings(), return the unique code for a bill_type ans sub_type pair      :param bill_type:, If we need to test for 404s or 405s this decorator can prevent the     request c

### Community 11 - "Price Calculation Model Tests"
Cohesion: 0.23
Nodes (3): create_test_price(), create_test_modifiers(), PriceTestCase

### Community 79 - "Viewer Application Configuration"
Cohesion: 0.67
Nodes (2): ViewerConfig, AppConfig

### Community 7 - "Scheme Presenter Helpers"
Cohesion: 0.10
Nodes (12): DelegatorMixin, Mixin to allow functions and properties to be delegated  Any calls to an unknown, Case type of the scenario          This can be, for example, Trial, Retrial, Cra, Filter collection for prices with this offence class, scheme_presenter_factory_from_pk(), SchemePresenter, Base type of the scheme - AGFS or LGFS          The base type of a scheme in the, Fetch list of prices for the scheme          The prices are filtered based on th (+4 more)

### Community 31 - "Offence Class Presenters"
Cohesion: 0.18
Nodes (5): offence_class_presenter_factory_from_pk(), _presenter_class(), OffenceClassPresenter, AlphaOffenceClassPresenter, Create an instance of an offence class presenter from a pk      Given the pk of

### Community 54 - "Abstract Offence Presenter"
Cohesion: 0.22
Nodes (4): AbstractOffenceClassPresenter, The label to be used in a form, The name as it should be displayed, Filter collection for prices with this offence class

### Community 61 - "Price Presenter Factory"
Cohesion: 0.33
Nodes (4): DelegatorMixin, price_presenter_factory(), PricePresenter, Generate a presenter for the price

### Community 10 - "Abstract Scenario Presenters"
Cohesion: 0.12
Nodes (7): ABC, scenario_presenter_factory_from_pk(), scenario_presenter_factory(), AbstractScenarioPresenter, NoneScenarioPresenter, NullScenarioPresenter, Create an instance of a scenario presenter from a pk      Given the pk of an ins

### Community 78 - "Numeric Offence Presenter"
Cohesion: 0.50
Nodes (1): NumericOffenceClassPresenter

### Community 47 - "Default Offence Presenter"
Cohesion: 0.20
Nodes (1): NoneOffenceClassPresenter

### Community 48 - "Null Offence Presenter"
Cohesion: 0.20
Nodes (1): NullOffenceClassPresenter

### Community 18 - "Scenario Presenter Tests"
Cohesion: 0.13
Nodes (3): ScenarioPresenter, WarrantScenarioPresenter, ScenarioPresenterTestCase

### Community 16 - "Null Scenario Presenter Tests"
Cohesion: 0.13
Nodes (3): InterimScenarioPresenter, NoneScenarioPresenterTestCase, NullScenarioPresenterTestCase

### Community 5 - "GOV.UK Component Framework"
Cohesion: 0.10
Nodes (16): isSupported(), isObject(), formatErrorMessage(), GOVUKFrontendError, SupportError, ConfigError, InitError, Component (+8 more)

### Community 8 - "Tabs and Skip Links"
Cohesion: 0.20
Nodes (3): getFragmentFromUrl(), SkipLink, Tabs

### Community 28 - "Responsive Navigation Components"
Cohesion: 0.19
Nodes (4): getBreakpoint(), ElementError, Header, ServiceNavigation

### Community 59 - "Accessible Error Notifications"
Cohesion: 0.32
Nodes (3): setFocus(), ErrorSummary, NotificationBanner

### Community 60 - "Internationalisation Plural Rules"
Cohesion: 0.43
Nodes (1): I18n

### Community 19 - "Accessible Accordion"
Cohesion: 0.26
Nodes (1): Accordion

### Community 20 - "Character Count Component"
Cohesion: 0.24
Nodes (2): closestAttributeValue(), CharacterCount

### Community 64 - "Conditional Checkbox Component"
Cohesion: 0.38
Nodes (1): Checkboxes

### Community 39 - "Exit Page Component"
Cohesion: 0.32
Nodes (1): ExitThisPage

### Community 40 - "Drag Drop File Upload"
Cohesion: 0.27
Nodes (2): FileUpload, isContainingFiles()

### Community 45 - "Conditional Input Components"
Cohesion: 0.27
Nodes (2): PasswordInput, Radios

### Community 12 - "MOJ Component Framework"
Cohesion: 0.15
Nodes (13): isObject(), GOVUKFrontendError, SupportError, ConfigError, t, ConfigurableComponent, normaliseString(), mergeConfigs() (+5 more)

### Community 46 - "Frontend Component Errors"
Cohesion: 0.29
Nodes (4): formatErrorMessage(), ElementError, InitError, Component

### Community 37 - "Repeatable Form Items"
Cohesion: 0.33
Nodes (1): AddAnother

### Community 76 - "Dismissible Alert Component"
Cohesion: 0.67
Nodes (2): setFocus(), Alert

### Community 30 - "Keyboard Button Menu"
Cohesion: 0.28
Nodes (1): ButtonMenu

### Community 2 - "Accessible Date Picker"
Cohesion: 0.10
Nodes (2): DatePicker, DSCalendarDay

### Community 26 - "Responsive Filter Toggle"
Cohesion: 0.23
Nodes (1): FilterToggleButton

### Community 23 - "Form Validation Component"
Cohesion: 0.25
Nodes (1): FormValidator

### Community 9 - "Multiple File Upload"
Cohesion: 0.13
Nodes (1): MultiFileUpload

### Community 62 - "Multi Select Component"
Cohesion: 0.43
Nodes (1): MultiSelect

### Community 77 - "Password Reveal Component"
Cohesion: 0.67
Nodes (1): PasswordReveal

### Community 27 - "Rich Text Editor"
Cohesion: 0.22
Nodes (1): RichTextEditor

### Community 67 - "Search Toggle Component"
Cohesion: 0.33
Nodes (1): SearchToggle

### Community 24 - "Sortable Table Component"
Cohesion: 0.28
Nodes (1): SortableTable

### Community 63 - "Offence Presenter Factory Tests"
Cohesion: 0.29
Nodes (1): OffenceClassPresenterFactoryTestCase

### Community 38 - "Alpha Offence Presenter Tests"
Cohesion: 0.17
Nodes (1): AlphaOffenceClassPresenterTestCase

### Community 44 - "Numeric Offence Presenter Tests"
Cohesion: 0.18
Nodes (1): NumericOffenceClassPresenterTestCase

### Community 43 - "Default Offence Presenter Tests"
Cohesion: 0.18
Nodes (1): NoneOffenceClassPresenterTestCase

### Community 49 - "Null Offence Presenter Tests"
Cohesion: 0.20
Nodes (1): NullOffenceClassPresenterTestCase

### Community 55 - "Scenario Presenter Factory Tests"
Cohesion: 0.22
Nodes (1): ScenarioPresenterFactoryTestCase

### Community 50 - "Interim Scenario Tests"
Cohesion: 0.20
Nodes (1): InterimScenarioPresenterTestCase

### Community 32 - "Warrant Scenario Tests"
Cohesion: 0.15
Nodes (1): WarrantScenarioPresenterTestCase

### Community 33 - "Scheme Presenter Tests"
Cohesion: 0.15
Nodes (2): SchemePresenterFactoryTestCase, SchemePresenterTestCase

### Community 80 - "Base Django Settings"
Cohesion: 0.67
Nodes (1): Django settings for fee_calculator project.  Generated by 'django-admin startpro

### Community 81 - "Project URL Routing"
Cohesion: 1.00
Nodes (1): fee_calculator URL Configuration  The `urlpatterns` list routes URLs to views. F

### Community 82 - "WSGI Application Configuration"
Cohesion: 1.00
Nodes (1): WSGI config for fee_calculator project.  It exposes the WSGI callable as a modul

### Community 25 - "Dependency Upgrade History"
Cohesion: 0.21
Nodes (14): 0131bce Merge pull request #690 from ministryofjustice/dependabot/pip/coverage-7.14.1, 09b16af Bump coverage from 7.14.0 to 7.14.1, 13ce67d Merge pull request #697 from ministryofjustice/dependabot/pip/idna-3.18, 2354b52 Bump rpds-py from 0.30.0 to 2026.5.1, 36e967f Merge pull request #694 from ministryofjustice/dependabot/github_actions/actions/checkout-6.0.3, 36f4896 Bump github/codeql-action from 4.36.0 to 4.36.2, 505a299 Merge pull request #686 from ministryofjustice/dependabot/pip/lxml-6.1.1, 5f3cb5c Merge pull request #691 from ministryofjustice/dependabot/github_actions/github/codeql-action-4.36.0 (+6 more)

### Community 36 - "Documentation and Dependency Updates"
Cohesion: 0.23
Nodes (12): 0183324 Merge pull request #742 from ministryofjustice/dependabot/github_actions/github/codeql-action/upload-sarif-4.37.9, 1a0cfb2 Add .github/copilot-instructions.md, 7525c3d Add links to hld and dfd, 80a40a3 Merge pull request #740 from ministryofjustice/add-hld-dfd-links, 86612f3 Merge pull request #738 from ministryofjustice/dependabot/pip/idna-3.19, 8a148b1 chore(deps): bump idna from 3.18 to 3.19, 8c4a893 Merge pull request #739 from ministryofjustice/mw/add-copilot-instructions, a8f9126 Merge pull request #725 from ministryofjustice/dependabot/pip/django-6.1 (+4 more)

### Community 14 - "Spring Dependency Updates"
Cohesion: 0.16
Nodes (18): 0193216 Merge pull request #685 from ministryofjustice/dependabot/pip/coverage-7.14.0, 1439628 Merge pull request #683 from ministryofjustice/dependabot/pip/requests-2.34.1, 4d2cfae Bump requests from 2.34.1 to 2.34.2, 4e47fff Bump requests from 2.33.1 to 2.34.1, 6585e24 Bump django from 6.0.4 to 6.0.5, 6791fc9 Bump coverage from 7.13.5 to 7.14.0, 7ae95c0 Merge pull request #684 from ministryofjustice/dependabot/pip/sentry-sdk-2.60.0, 7d6352c Bump sentry-sdk from 2.59.0 to 2.60.0 (+10 more)

### Community 4 - "Scheme Development History"
Cohesion: 0.11
Nodes (37): 02c5dc7 fix(env): remove environment req from deploy step, 0a5e4e3 fix: amend SHAs to the correct version, 2b078e6 Add Additional Prep Fee prices for Guilty Pleas, 2d17789 Add AGFS Fee Scheme 17, 2ec01cd chore(ci): add region link back, 3a05e37 fix: edit kube config step, 3b7b6f5 Add AGFS Fee Scheme 17 prices, 481f0a4 fix(cert): fix token input line (+29 more)

### Community 17 - "Summer Dependency Updates"
Cohesion: 0.18
Nodes (16): 09ef7fb Merge pull request #701 from ministryofjustice/dependabot/pip/sentry-sdk-2.63.0, 18c6757 Bump rpds-py from 2026.5.1 to 2026.6.3, 1efded4 Bump django from 6.0.5 to 6.0.6, 20937c1 Bump rtCamp/action-slack-notify from 2.3.3 to 2.4.0, 30ebba8 Merge pull request #698 from ministryofjustice/dependabot/pip/sentry-sdk-2.62.0, 3191286 Merge pull request #692 from ministryofjustice/dependabot/pip/sentry-sdk-2.61.1, 4ea3a56 Merge pull request #707 from ministryofjustice/dependabot/pip/rpds-py-2026.6.3, 5c5755b Bump actions/checkout from 6.0.3 to 7.0.0 (+8 more)

### Community 22 - "Build and Dependency Maintenance"
Cohesion: 0.18
Nodes (15): 1671d6b chore(deps): bump github/codeql-action/upload-sarif, 1c3d3c2 chore(deps): bump actions/setup-python from 6 to 7, 361e98b test build, 3b6c2f9 Merge pull request #728 from ministryofjustice/dependabot/github_actions/actions/setup-python-7, 645ab54 test build, 68e7035 Merge pull request #700 from ministryofjustice/chore/CTSKF-1682-add-github-actions, 9f9179a Merge pull request #727 from ministryofjustice/dependabot/pip/sqlparse-0.6.0, d0573ff Merge pull request #729 from ministryofjustice/dependabot/github_actions/actions/cache-6 (+7 more)

### Community 6 - "CI Workflow History"
Cohesion: 0.13
Nodes (30): 1901a07 chore(ci): add initial tests to a github workflow, 1dd6d92 chore(ci): set include hidden files to true, 2cc5f6f chore(ci): remove branch line from triggers, 328a7c9 chore(ci): remove lint tests combine from circleci, 3d8629c chore(ci): fix sharded tests to 3 different shards, 40074c4 chore(ci): update actions versions exc download, 4b39ab0 chore(ci): add check for cov files to view api set, 4db67b5 chore(ci): change upload to v7 (+22 more)

### Community 29 - "Latest Dependency Updates"
Cohesion: 0.23
Nodes (13): 23fbea5 Merge pull request #726 from ministryofjustice/dependabot/pip/drf-nested-routers-0.95.3, 4ac3167 chore(deps-dev): bump coverage from 7.15.2 to 7.15.4, 5bcdae7 chore(deps-dev): bump lxml from 6.1.1 to 6.1.2, 5f3630f Merge pull request #735 from ministryofjustice/dependabot/github_actions/aws-actions/amazon-ecr-login-2.1.7, 6528092 Merge pull request #731 from ministryofjustice/dependabot/pip/djangorestframework-3.18.0, 724d6c8 Merge pull request #737 from ministryofjustice/dependabot/pip/charset-normalizer-3.5.1, 72ab2d3 chore(deps): bump aws-actions/amazon-ecr-login from 2.1.6 to 2.1.7, 81e0ac2 chore(deps): bump djangorestframework from 3.17.1 to 3.18.0 (+5 more)

### Community 42 - "Security Dependency Updates"
Cohesion: 0.27
Nodes (11): 37139ce Bump github/codeql-action from 4.35.2 to 4.35.4, 3b34024 Merge pull request #674 from ministryofjustice/dependabot/pip/sentry-sdk-2.58.0, 62808fb Merge pull request #667 from ministryofjustice/ctskf-1522-update-django, 6aaece3 Bump idna from 3.11 to 3.13, 6f01d22 Bump ministryofjustice/devsecops-actions from 1.5.0 to 1.6.0, a9a9ec6 Merge pull request #681 from ministryofjustice/dependabot/github_actions/github/codeql-action-4.35.4, baf2652 Merge pull request #676 from ministryofjustice/dependabot/pip/idna-3.13, d4566f5 Merge pull request #680 from ministryofjustice/dependabot/github_actions/ministryofjustice/devsecops-actions-1.6.0 (+3 more)

### Community 58 - "Monitoring Dependency Updates"
Cohesion: 0.36
Nodes (8): 6cd6a44 Merge pull request #705 from ministryofjustice/dependabot/pip/sentry-sdk-2.64.0, 8d38339 Bump sentry-sdk from 2.63.0 to 2.64.0, a794e78 Merge pull request #710 from ministryofjustice/dependabot/pip/charset-normalizer-3.4.9, ad94d16 Merge pull request #709 from ministryofjustice/dependabot/github_actions/github/codeql-action/upload-sarif-4.37.0, c695d1a Merge pull request #704 from ministryofjustice/dependabot/pip/coverage-7.14.3, c70a419 Bump coverage from 7.14.1 to 7.14.3, c9a6c22 Bump charset-normalizer from 3.4.7 to 3.4.9, c9c9637 Bump github/codeql-action/upload-sarif from 4.36.3 to 4.37.0

### Community 144 - "Pull Request Template"
Cohesion: 1.00
Nodes (1): Pull Request Template

### Community 127 - "GOV.UK Black Favicon"
Cohesion: 1.00
Nodes (1): GOV.UK Black Crown Favicon

### Community 128 - "GOV.UK Royal Crest"
Cohesion: 1.00
Nodes (1): GOV.UK Royal Coat of Arms Crest

### Community 129 - "GOV.UK Crown 180px"
Cohesion: 1.00
Nodes (1): GOV.UK Crown Icon 180px

### Community 130 - "GOV.UK Crown 192px"
Cohesion: 1.00
Nodes (1): GOV.UK Crown Icon 192px

### Community 131 - "GOV.UK Crown 512px"
Cohesion: 1.00
Nodes (1): GOV.UK Crown Icon 512px

### Community 132 - "GOV.UK Mask Icon"
Cohesion: 1.00
Nodes (1): GOV.UK Crown Mask Icon

### Community 133 - "GOV.UK Social Image"
Cohesion: 1.00
Nodes (1): GOV.UK Open Graph Image

### Community 145 - "Rebranded GOV.UK Favicon"
Cohesion: 1.00
Nodes (1): Rebranded GOV.UK Blue Crown Favicon

### Community 146 - "Rebranded GOV.UK Crest"
Cohesion: 1.00
Nodes (1): Rebranded GOV.UK Royal Coat of Arms Crest

### Community 66 - "GOV.UK App Branding"
Cohesion: 0.33
Nodes (6): GOV.UK Crown App Icon 180px, GOV.UK Crown App Icon 192px, GOV.UK Crown App Icon 512px, GOV.UK Crown Mask Icon, GOV.UK Open Graph Brand Image, GOV.UK Logotype Crown

### Community 73 - "Status Alert Icons"
Cohesion: 0.40
Nodes (5): Information Alert Icon, Success Alert Icon, Warning Alert Icon, Progress Tick Icon PNG, Progress Tick Icon SVG

### Community 74 - "Directional Control Icons"
Cohesion: 0.50
Nodes (5): Black Down Arrow Icon, Black Up Arrow Icon, White Down Arrow Icon, White Up Arrow Icon, Black Close Cross Icon

### Community 112 - "Document Format Icons"
Cohesion: 1.00
Nodes (2): Document Icon PNG, Document Icon SVG

### Community 113 - "Search Colour Icons"
Cohesion: 1.00
Nodes (2): Black Search Icon, Blue Search Icon

### Community 120 - "White Search Icon"
Cohesion: 1.00
Nodes (1): White Search Icon

### Community 83 - "Tag Removal Icons"
Cohesion: 1.00
Nodes (2): White Tag Removal Cross Icon, Tag Removal Cross Icon

### Community 121 - "Toggle State Icon"
Cohesion: 1.00
Nodes (1): Plus and Minus Toggle Icon

### Community 122 - "Editor Bold Icon"
Cohesion: 1.00
Nodes (1): WYSIWYG Bold Icon

### Community 123 - "Editor Italic Icon"
Cohesion: 1.00
Nodes (1): WYSIWYG Italic Icon

### Community 124 - "Editor Ordered List Icon"
Cohesion: 1.00
Nodes (1): WYSIWYG Ordered List Icon

### Community 125 - "Editor Underline Icon"
Cohesion: 1.00
Nodes (1): WYSIWYG Underline Icon

### Community 126 - "Editor Unordered List Icon"
Cohesion: 1.00
Nodes (1): WYSIWYG Unordered List Icon

### Community 138 - "MOJ Touch Icon 152px"
Cohesion: 1.00
Nodes (1): MOJ Apple Touch Icon 152×152 (2024)

### Community 139 - "MOJ Touch Icon 167px"
Cohesion: 1.00
Nodes (1): MOJ Apple Touch Icon 167×167 (2024)

### Community 140 - "MOJ Touch Icon 180px"
Cohesion: 1.00
Nodes (1): MOJ Apple Touch Icon 180×180 (2024)

### Community 141 - "MOJ Touch Icon 120px"
Cohesion: 1.00
Nodes (1): MOJ Apple Touch Icon 120×120 (2024)

### Community 114 - "MOJ Crest Marks"
Cohesion: 1.00
Nodes (2): MOJ Crest Raster Mark (2024), MOJ Crest Vector Mark (2024)

### Community 142 - "MOJ Social Image 2024"
Cohesion: 1.00
Nodes (1): MOJ Open Graph Image (2024)

## Knowledge Gaps
- **74 isolated node(s):** `Loads fixtures files for a given label. This method is largely copied         fr`, `Migration`, `Migration`, `Migration`, `Migration` (+69 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Advocate Type API Tests`** (1 nodes): `AdvocateTypeApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Price API Tests`** (2 nodes): `APITestCase`, `PriceApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fee Type API Tests`** (1 nodes): `FeeTypeApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scheme Filter Tests`** (1 nodes): `SchemeFilterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Modifier Type API Tests`** (1 nodes): `ModifierTypeApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Offence Class API Tests`** (1 nodes): `OffenceClassApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scenario API Tests`** (1 nodes): `ScenarioApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scheme API Tests`** (1 nodes): `SchemeApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Unit API Tests`** (1 nodes): `UnitApiTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Advocate Category Compatibility`** (1 nodes): `FixAdvocateCategoryTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0001 Initial Schema`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0002 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0003 Scenario Cleanup`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0004 Price Cleanup`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0005 Fixed Fees`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0006 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0007 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0008 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0009 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0010 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0011 Scheme Dates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0012 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0013 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0014 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0015 Required Modifiers`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0016 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0017 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0018 Strict Modifiers`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0019 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0020 Fee Aggregation`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0021 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0022 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0023 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0024 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0025 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0026 Strict Prices`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0027 Model Updates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration 0028 Hearing Dates`** (1 nodes): `Migration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Viewer Application Configuration`** (2 nodes): `ViewerConfig`, `AppConfig`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Numeric Offence Presenter`** (1 nodes): `NumericOffenceClassPresenter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Default Offence Presenter`** (1 nodes): `NoneOffenceClassPresenter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Null Offence Presenter`** (1 nodes): `NullOffenceClassPresenter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Internationalisation Plural Rules`** (1 nodes): `I18n`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Accordion`** (1 nodes): `Accordion`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Character Count Component`** (2 nodes): `closestAttributeValue()`, `CharacterCount`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Conditional Checkbox Component`** (1 nodes): `Checkboxes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Exit Page Component`** (1 nodes): `ExitThisPage`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Drag Drop File Upload`** (2 nodes): `FileUpload`, `isContainingFiles()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Conditional Input Components`** (2 nodes): `PasswordInput`, `Radios`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Repeatable Form Items`** (1 nodes): `AddAnother`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dismissible Alert Component`** (2 nodes): `setFocus()`, `Alert`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Keyboard Button Menu`** (1 nodes): `ButtonMenu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Date Picker`** (2 nodes): `DatePicker`, `DSCalendarDay`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Responsive Filter Toggle`** (1 nodes): `FilterToggleButton`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Form Validation Component`** (1 nodes): `FormValidator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Multiple File Upload`** (1 nodes): `MultiFileUpload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Multi Select Component`** (1 nodes): `MultiSelect`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Password Reveal Component`** (1 nodes): `PasswordReveal`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rich Text Editor`** (1 nodes): `RichTextEditor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Search Toggle Component`** (1 nodes): `SearchToggle`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sortable Table Component`** (1 nodes): `SortableTable`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Offence Presenter Factory Tests`** (1 nodes): `OffenceClassPresenterFactoryTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Alpha Offence Presenter Tests`** (1 nodes): `AlphaOffenceClassPresenterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Numeric Offence Presenter Tests`** (1 nodes): `NumericOffenceClassPresenterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Default Offence Presenter Tests`** (1 nodes): `NoneOffenceClassPresenterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Null Offence Presenter Tests`** (1 nodes): `NullOffenceClassPresenterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scenario Presenter Factory Tests`** (1 nodes): `ScenarioPresenterFactoryTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Interim Scenario Tests`** (1 nodes): `InterimScenarioPresenterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Warrant Scenario Tests`** (1 nodes): `WarrantScenarioPresenterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scheme Presenter Tests`** (2 nodes): `SchemePresenterFactoryTestCase`, `SchemePresenterTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Base Django Settings`** (1 nodes): `Django settings for fee_calculator project.  Generated by 'django-admin startpro`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project URL Routing`** (1 nodes): `fee_calculator URL Configuration  The `urlpatterns` list routes URLs to views. F`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `WSGI Application Configuration`** (1 nodes): `WSGI config for fee_calculator project.  It exposes the WSGI callable as a modul`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pull Request Template`** (1 nodes): `Pull Request Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GOV.UK Black Favicon`** (1 nodes): `GOV.UK Black Crown Favicon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GOV.UK Royal Crest`** (1 nodes): `GOV.UK Royal Coat of Arms Crest`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GOV.UK Crown 180px`** (1 nodes): `GOV.UK Crown Icon 180px`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GOV.UK Crown 192px`** (1 nodes): `GOV.UK Crown Icon 192px`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GOV.UK Crown 512px`** (1 nodes): `GOV.UK Crown Icon 512px`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GOV.UK Mask Icon`** (1 nodes): `GOV.UK Crown Mask Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GOV.UK Social Image`** (1 nodes): `GOV.UK Open Graph Image`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rebranded GOV.UK Favicon`** (1 nodes): `Rebranded GOV.UK Blue Crown Favicon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rebranded GOV.UK Crest`** (1 nodes): `Rebranded GOV.UK Royal Coat of Arms Crest`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Document Format Icons`** (2 nodes): `Document Icon PNG`, `Document Icon SVG`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Search Colour Icons`** (2 nodes): `Black Search Icon`, `Blue Search Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `White Search Icon`** (1 nodes): `White Search Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tag Removal Icons`** (2 nodes): `White Tag Removal Cross Icon`, `Tag Removal Cross Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Toggle State Icon`** (1 nodes): `Plus and Minus Toggle Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Editor Bold Icon`** (1 nodes): `WYSIWYG Bold Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Editor Italic Icon`** (1 nodes): `WYSIWYG Italic Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Editor Ordered List Icon`** (1 nodes): `WYSIWYG Ordered List Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Editor Underline Icon`** (1 nodes): `WYSIWYG Underline Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Editor Unordered List Icon`** (1 nodes): `WYSIWYG Unordered List Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MOJ Touch Icon 152px`** (1 nodes): `MOJ Apple Touch Icon 152×152 (2024)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MOJ Touch Icon 167px`** (1 nodes): `MOJ Apple Touch Icon 167×167 (2024)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MOJ Touch Icon 180px`** (1 nodes): `MOJ Apple Touch Icon 180×180 (2024)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MOJ Touch Icon 120px`** (1 nodes): `MOJ Apple Touch Icon 120×120 (2024)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MOJ Crest Marks`** (2 nodes): `MOJ Crest Raster Mark (2024)`, `MOJ Crest Vector Mark (2024)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MOJ Social Image 2024`** (1 nodes): `MOJ Open Graph Image (2024)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Scheme` connect `Fee Calculator Data Models` to `Fee Uplift Commands`, `Scheme Presenter Helpers`, `Scheme Presenter Tests`, `Advocate Type API Tests`, `Fee Type API Tests`, `Scheme Filter Tests`, `Price Calculation Model Tests`, `Modifier Type API Tests`, `Offence Class API Tests`, `Scenario API Tests`, `Unit API Tests`, `Advocate Category Compatibility`, `Viewer Page Tests`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `OffenceClass` connect `Fee Calculator Data Models` to `Abstract Offence Presenter`, `Offence Class Presenters`, `Default Offence Presenter`, `Null Offence Presenter`, `Numeric Offence Presenter`, `Alpha Offence Presenter Tests`, `Default Offence Presenter Tests`, `Null Offence Presenter Tests`, `Numeric Offence Presenter Tests`, `Offence Presenter Factory Tests`, `Price Calculation Model Tests`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `Price` connect `Fee Calculator Data Models` to `Fee Uplift Commands`, `Calculator Fee Test Framework`, `Price Calculation Model Tests`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 78 inferred relationships involving `Scheme` (e.g. with `AdvocateTypeSerializer` and `BasePriceFilteredQuerySerializer`) actually correct?**
  _`Scheme` has 78 INFERRED edges - model-reasoned connections that need verification._
- **Are the 75 inferred relationships involving `Price` (e.g. with `AdvocateTypeSerializer` and `BasePriceFilteredQuerySerializer`) actually correct?**
  _`Price` has 75 INFERRED edges - model-reasoned connections that need verification._
- **Are the 68 inferred relationships involving `FeeType` (e.g. with `AdvocateTypeSerializer` and `BasePriceFilteredQuerySerializer`) actually correct?**
  _`FeeType` has 68 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Loads fixtures files for a given label. This method is largely copied         fr`, `Migration`, `Migration` to the rest of the system?**
  _74 weakly-connected nodes found - possible documentation gaps or missing edges._