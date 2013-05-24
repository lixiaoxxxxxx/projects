from __future__ import division
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils.encoding import smart_unicode
from django.core.serializers import serialize,deserialize
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.utils import simplejson
#from django.views.decorators.csrf import csrf_exempt
import unicodedata
import time
import string
import os, sys
import json
import re
import pickle as pk
from grouping.models import * 
from grouping.NCdetection_v2 import *
from grouping.test import *

def hello_world(request):
	try:
		uid = int(request.GET.get('query'))
		NCdetection(uid)
		nc, neighbors = test_g(uid)
	except:
		uid = ""
		nc, neighbors = test_g(uid)
		#return render_to_response('grouping.html', {
		#}, context_instance=RequestContext(request))
		pass
	print neighbors
	nc_list_1 = [{'label':x, 'uid_list':y, 'member_number': len(y)} for x,y in nc]
	for item in nc_list_1:
		temp = [{'uid': x, 'No': y, 'name': z, 'is_neighbor': x in neighbors} for x,y,z in item['uid_list']]
		item['uid_list'] = temp
	return render_to_response('grouping.html', {
		'image': 'result/' + str(uid) + '_xx.png',
		'nc': nc_list_1
	}, context_instance=RequestContext(request))
	return HttpResponse('hello')

def hello_world_force(request):
	g_json = json_g()
	#g_json = {"nodes":g_json["nodes"], "links":[]}
	g_json = simplejson.dumps(g_json)
	
	return HttpResponse(g_json)
	pass


#def get_dir():
	##current_directory = os.getcwd() + "/girlsMining"
	#current_directory = "/var/www/girlsMining/girlsMining"
	#folder_name = current_directory + "/raw_material/"
#def hello_world(request):
	#1/0
	#return HttpResponse("hello")
#def update(request):
	#id_all = get_id_all()
	#temp = ""
	#for item in id_all:
		#xx = wb(item)
		#try:
			#Infomation.objects.get(userid=xx.id)
		#except Infomation.DoesNotExist:
			#Infomation.objects.create(userid=xx.id, name=xx.name.encode('utf-8'), follower_count=xx.follower_count, friend_count=xx.friend_count, mf_rate=xx.mf_rate, statuses_count=xx.statuses_count, statuses_pic_rate=xx.statuses_pic_rate)
			#for item1 in xx.status_list:
				#try:
					#Status.objects.create(text=item1.text.encode('utf-8'), client=item1.client, comments_count=item1.comments_count, reposts_count=item1.reposts_count, pic_big=item1.pic_big, pic_small=item1.pic_small, very_small=item1.very_small, FK_user=Infomation.objects.get(userid=xx.id))
				#except:
					#pass
		##if len(xx.status_list) > 6:
			##xx.status_list = xx.status_list[0:6]
		##for text in xx.status_list:
			##text.text = ""
		##try:
			##temp = Infomation.objects.get(userid=xx.id)
			##temp1 = temp.status_set.all()
			##for temp2 in temp1:
				##haha.append(temp2.text)
		##except Status.DoesNotExist:
			##pass
#
	#return HttpResponse("hello")
#
#def girlsmining(request):
	##id_all = get_id_all()
	#user_all = Infomation.objects.all()
	#s = ""
	#girls = []
	#per_page_number = 10
	#haha = []
	##update()
	#page = 0
#
	#if request.method == 'GET':
		#try: 
			#page = int(request.GET.get('page'))
			#start = page * per_page_number
			#if start < len(user_all):
				#if start + per_page_number < len(user_all):
					#end = start + per_page_number
				#else:
					#end = len(user_all)
				#for item in user_all[start:end]:
					##xx = wb(item)
					##try:
						##Infomation.objects.get(userid=xx.id)
					##except Infomation.DoesNotExist:
						##Infomation.objects.create(userid=xx.id, name=xx.name.encode('utf-8'), follower_count=xx.follower_count, friend_count=xx.friend_count, mf_rate=xx.mf_rate, statuses_count=xx.statuses_count, statuses_pic_rate=xx.statuses_pic_rate)
						##for item1 in xx.status_list:
							##try:
								##Status.objects.create(text=item1.text.encode('utf-8'), client=item1.client, comments_count=item1.comments_count, reposts_count=item1.reposts_count, pic_big=item1.pic_big, pic_small=item1.pic_small, very_small=item1.very_small, FK_user=Infomation.objects.get(userid=xx.id))
							##except:
								##pass
					##if len(xx.status_list) > 6:
						##xx.status_list = xx.status_list[0:6]
					#item.status_list = item.status_set.filter(FK_user=item.id)
					#if len(item.status_list) > 6:
						#item.status_list = item.status_list[0:6]
					##try:
						##temp = Infomation.objects.get(userid=xx.id)
						##temp1 = temp.status_set.all()
						##for temp2 in temp1:
							##haha.append(temp2.text)
					##except Status.DoesNotExist:
						##pass
					#girls.append(item)
		#except:
			#userid = request.GET.get('id')
			#girls = Infomation.objects.filter(userid=userid)
			#girls[0].status_list = girls[0].status_set.filter(FK_user=girls[0].id)
			#pass
	#pages = range(0, int((len(user_all) - 1) / per_page_number) + 1)
	#pre_page = None
	#next_page = None
	#if (page > 0): 
		#pre_page = page - 1
	#if (page < int((len(user_all) - 1) / per_page_number)): 
		#next_page = 1 + page
	#
	#return render_to_response('girls.html', {
		#'girls': girls,
		#'cur_page': page,
		#'pre_page': pre_page,
		#'next_page': next_page,
		#'pages': pages,
		#'haha': haha,
		##'dir': dir,
	#}, context_instance=RequestContext(request))
#
#@csrf_exempt
#def classify(request):
	#try:
		#userid = request.POST.get('userid')
		#value = request.POST.get('value')
		#Infomation.objects.filter(userid=userid).update(category=value)
	#except:
		#pass
	#return HttpResponse("hello")
#
#def test(request):
	#Infomation.objects.filter(name__contains=u'\u624b\u673a\u7528\u6237').update(category=3)
	#return HttpResponse("hello")
	#pass
#
#def find_robots(request):
	#user_all = Infomation.objects.all()
	#for user in user_all:
		#if user.category == None:
			##return HttpResponse(user.id)
			#user.status_list = user.status_set.filter(FK_user=user.id)
			#repost_number = 0
			#for status in user.status_list:
				##txt = status.text
				##1/0
				#if is_repost(status.text):
					#repost_number += 1
				#if check_if_robot_v2(name = user.name, friends_count = user.friend_count, follower_count = user.follower_count, statuses_number = len(user.status_list), repost_number = repost_number):
					#Infomation.objects.filter(userid=user.userid).update(category=3)
	#return HttpResponse("hello")
	#pass
#
#def set_status_info(request):
	#user_all = Infomation.objects.all()
	#for user in user_all:
		#user.status_list = user.status_set.filter(FK_user=user.id)
		##xx = user.status_list[1].client.find(u'\u5ba2\u6237')
		##return HttpResponse(str(xx))
		##1/0
		#client = get_client(user.status_list)
		#comments_count_avg = get_comments_count_avg(user.status_list)
		#reposts_count_avg = get_reposts_count_avg(user.status_list)
		#userid = user.userid
		#Infomation.objects.filter(id=user.id).update(client=client, comments_count_avg=comments_count_avg, reposts_count_avg=reposts_count_avg)
	#pass
	#return HttpResponse('hello')
#
#def check_client(client):
	#level = 0
	#for item in ["Symbian", "S60", "Nokia", "nokia", u'\u8bfa\u57fa\u4e9a']:
		#if client.find(item) > -1:
			#level = 1
	#for item in ["Win"]:
		#if client.find(item) > -1:
			#level = 2
	#for item in ["Android", "HTC", "android", "MOTO", u'\u5c0f\u7c73', u'\u4e2d\u5174', u'\u534e\u4e3a', u'\u4e09\u661f', u'\u667a\u80fd\u624b\u673a']: 
		#if client.find(item) > -1:
			#level = 3
	#for item in ["iPhone", "iPad"]:
		#if client.find(item) > -1:
			#level = 4
	#return level
	#pass
#
#def get_client(status_list):
	#level = 0
	#for status in status_list:
		#xx = check_client(status.client)
		#if (xx > level):
			#level = xx
	#if level == 4:
		#return "iphone"
	#elif level == 3:
		#return "android"
	#elif level == 2:
		#return "win"
	#elif level == 1:
		#return "symbian"
	#else:
		#return "browser"
#def get_comments_count_avg(status_list):
	#total = 0
	#for status in status_list:
		#total += status.comments_count
	#if (len(status_list) > 0):
		#return total / len(status_list)
	#else:
		#return 0
#
#def get_reposts_count_avg(status_list):
	#total = 0
	#for status in status_list:
		#total += status.reposts_count
	#if (len(status_list) > 0):
		#return total / len(status_list)
	#else:
		#return 0
