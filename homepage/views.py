from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def top(request):
    html = loader.render_to_string('homepage/top.html')
    return HttpResponse(html)
