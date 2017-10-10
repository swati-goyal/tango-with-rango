from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render_to_response('C:\\Users\swati.goyal\\tango_with_django_project\\templates\\rango\\index.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    context_dict = {'boldaboutmessage': "This is about page!"}
    return render_to_response('C:\\Users\swati.goyal\\tango_with_django_project\\templates\\rango\\about.html', context_dict, context)


