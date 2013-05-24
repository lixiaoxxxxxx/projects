# Create your views here.
from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
import datetime
from lab2.models import *

def book_room(code, start_time, end_time, room_id):
	if code == "":
		return
	else:
		room = Room.objects.filter(id = room_id)[0]
		room.start_time = start_time
		room.end_time = end_time
		room.booker = code
		room.state = "booked"
		room.save()
		print "room booked"

def book_cancel(room_id):
	room = Room.objects.filter(id = room_id)[0]
	#room.start_time = ""
	#room.end_time = ""
	room.booker = ""
	room.state = "available"
	room.save()
	print "room booked canceled"

def about(request):
	t = {"title" : "About",
			"in_about" : True,
			"about_state" : "active",
			"about" : "About what?"}
	return render(request, 'lab2_index.html', t)



def query(request):
	t = {'query_state' : "active",
			"in_query" : True,
			"title" : "Query"}
	code = -1
	if "room_id" in request.POST:
		book_cancel(request.POST["room_id"])
	if "search" in request.GET:
		code = request.GET["search"]
		if code != "":
			rooms = Room.objects.filter(booker = code)
			t["rooms"] = rooms

	return render(request, "lab2_index.html", t)
	#return render_to_response(request, "lab2_index.html", t, context_instance=RequestContext(request))

def reserve(request):
	post = request.POST
	get = request.GET
	if "code" in post:
		code = post["code"]
		if code != "":
			book_room(code, post["start-time"], post["end-time"], get["Room"])
			

	today = datetime.date.today()
	t = {	"in_reserve" : True,
			"title" : "Reserve"}
	if "Room" in get:
		t["room"] = Room.objects.filter(id = get["Room"])[0]
	t["today"] = str(today)
	return render(request, "lab2_index.html", t)

def home(request):
	t = {'home_state' : "active",
			"in_home" : True,
			"title" : "Home"}

	hotels = Hotel.objects.all()
	hotel_name = set()
	city_name = set()
	for h in hotels:
		hotel_name.add(h.name)
		city_name.add(h.city)
	t["hotels"] = hotel_name
	t["citys"] = city_name 

	if "hotel" in request.GET:
		_name = request.GET["hotel"]
		if _name != "":
			hotels = hotels.filter(name = _name)
	if "city" in request.GET:
		_city= request.GET["city"]
		if _city != "":
			hotels = hotels.filter(city = _city)
	print "hotels: ", hotels
	rooms = Room.objects.filter(state = "available")
	room_final = []
	for r in rooms:
		if r.hotel in hotels:
			room_final.append(r)
	print "rooms: ", room_final
	t["rooms"] = room_final

	return render(request, 'lab2_index.html', t)
