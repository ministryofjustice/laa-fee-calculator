web: ./manage.py runserver "0.0.0.0:$PORT" --settings=fee_calculator.settings.heroku --noreload
migrate: ./manage.py migrate calculator --settings=fee_calculator.settings.heroku
loaddata: ./manage.py loaddata fee_calculator/apps/calculator/fixtures/*.yaml  --settings=fee_calculator.settings.heroku
