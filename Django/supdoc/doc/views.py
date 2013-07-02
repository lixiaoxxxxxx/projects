# Create your views here.

from django.template import Template, Context
from django.shortcuts import render
from django.shortcuts import render_to_response
import datetime
from random import choice, randint

from doc.models import *
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

#def ajax(request):
	#get = GET
	#print get
	#return

def home(request):
	t = {}
	t["title"] = "Doc!"
	nd = Doc_file(name = "test", content = "hello world")
	nd.save()
	fs = Doc_file.objects.all()
	t["files"] = fs
	return render(request, 'doc.html', t)

def ajax_write(request):
	get = request.GET
	f = open("content", "wb")
	f.write(get["content"])
	f.close()
	return HttpResponse("done")

def ajax_fetch(request):
	f = open("content", "rb")
	t = {}
	t["content"] = f.read()
	f.close()
	return HttpResponse(simplejson.dumps(t))

def get_msg(request):
	f = open("chat", "rb")
	content = f.readlines()
	f.close()
	t = {}
	t["msg"] = content
	print content
	return HttpResponse(simplejson.dumps(t))

def send_msg(request):
	get = request.GET
	f = open("chat", "a")
	f.write(get["_name"] + " : " + get["_msg"] + "\n")
	f.close()
	return HttpResponse("done")


