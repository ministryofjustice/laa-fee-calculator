web: ./manage.py collectstatic --noinput --settings=fee_calculator.settings.heroku; DJANGO_SETTINGS_MODULE=fee_calculator.settings.heroku uwsgi --ini uwsgi.ini --http-socket=:$PORT
migrate: ./manage.py migrate calculator --settings=fee_calculator.settings.heroku
loaddata: ./manage.py loaddata fee_calculator/apps/calculator/fixtures/*.yaml  --settings=fee_calculator.settings.heroku
