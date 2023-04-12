from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class Stat(TemplateView):
    template_name = 'admin/statistic.html'






