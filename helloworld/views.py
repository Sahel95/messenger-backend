from django.http import HttpResponse

def index(request):
    response = HttpResponse(
        "Hello World"
    )
    return response

def bye(request):
    response = HttpResponse(
        "Bye Bye"
    )
    return response    