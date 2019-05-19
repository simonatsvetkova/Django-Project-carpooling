from django.http import HttpResponse

def home_page(request):
	return HttpResponse("<h1>Hello world</h1>")


def about_page(request):
	return HttpResponse("About")

def contact_page(request):
	return HttpResponse("About")