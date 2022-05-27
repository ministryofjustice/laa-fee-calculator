from django.shortcuts import render

from calculator.models import Scheme


def index(request):
    return render(request, 'viewer/index.html')


def fee_schemes(request):
    schemes = Scheme.objects.all

    return render(request, 'viewer/fee_schemes.html', {'schemes': schemes})
