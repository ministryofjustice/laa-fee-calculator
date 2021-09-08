import os
import datetime

from django.core.exceptions import ImproperlyConfigured
from django.http.response import JsonResponse
from django.views.generic import View


def current_utctime_in_range(start, end):
    """Returns whether current is in the range [start, end]"""
    return start <= datetime.datetime.utcnow().time() <= end

class FailingPingJsonView(View):
    """
    View for returning IRaT information from environment variables
    c.f. https://github.com/ministryofjustice/incident-response-schemas/blob/master/ping-dot-json-schema.json

    Usage:
        urlpatterns = [
            ...
            url(r'^ping.json$', PingJsonView.as_view(**environment_key_names), name='ping_json'),
            ...
        ]
    """
    build_date_key = None      # Docker container build date
    commit_id_key = None       # Git SHA from which the image was built
    version_number_key = None  # Docker container tag
    build_tag_key = None       # Jenkins job name and id

    def __init__(self, **kwargs):
        if not kwargs.get('build_date_key') or not kwargs.get('commit_id_key'):
            raise ImproperlyConfigured('ping.json schema requires build_date_key and '
                                       'commit_id_key to be provided')
        super(FailingPingJsonView, self).__init__(**kwargs)

    def get(self, request):
        response_data = {
            attr[:-4]: os.environ.get(getattr(self, attr))
            for attr in dir(self)
            if attr.endswith('_key') and getattr(self, attr)
        }
        response = JsonResponse(response_data)

        utcstart = datetime.time(9, 10, 0)
        utcend = datetime.time(9, 15, 0)
        if current_utctime_in_range(utcstart, utcend):
            response.status_code = 503
        elif not response_data['build_date'] or not response_data['commit_id']:
            response.status_code = 501

        response['Access-Control-Allow-Origin'] = '*'

        return response
