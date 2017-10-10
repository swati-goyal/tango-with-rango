from django.http import HttpResponse


def main_index(request):
    return HttpResponse("This is the main page!")
