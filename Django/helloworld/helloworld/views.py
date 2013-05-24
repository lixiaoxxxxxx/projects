from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from blog.models import *
import datetime

def hello(request):
	return HttpResponse("Hello world")

def home(request):
	t = get_template("index.html")
	html = t.render(Context({'content' : "this is the home page",
								'home_state' : "active"}))
	return HttpResponse(html)

def blog(request):
	t = get_template("index.html")
	if "search" in request.GET:
		print "Asdasd"
	html = t.render(Context({'content' : "hello everyone",
								'blog_state' : "active",
								"in_blog" : True}))
	return HttpResponse(html)

def search_form(request):
    return render(request, 'search_form.html')

def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		blogs = Blog.objects.filter(title__icontains=q)
		return render(request, 'search_result.html',
				{'blogs': blogs, 'query': q})
	else:
		return HttpResponse('Please submit a search term.')	

def time(request):
	time = datetime.datetime.now()
	t = get_template("time.html")
	html = t.render(Context({'time' : time}))
	return HttpResponse(html)

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()

	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)

	html = "<html><body> it will be %s. </body> </html>" % dt 
	return HttpResponse(html)


def browser(request):
	ua = request.META.get('HTTP_USER_AGENT', 'unknown')
	return HttpResponse("Your browser is %s" % ua)
