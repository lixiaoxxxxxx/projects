# -*- coding: utf-8 -*-
import unicodedata
import time
import string
import os, sys
import json
import urllib2
import re
import random
import pickle as pk
import networkx as nx
#from weibo import APIClient
#from get_code import *
#from lp import *
from grouping.draw import *
from grouping.get_code import *
from grouping.weibo import APIClient
from grouping.models import *
#from NCdetection_v2 import *

g = nx.Graph()
expanded = []

def token(): 
	r = client.request_access_token(get_code())
	client.set_access_token(r.access_token, r.expires_in)

def del_x_degree_node(x):
	global g
	global expanded
	degree_list = nx.degree(g)
	degree_list = sorted(degree_list.iteritems(), key = lambda asd:asd[1])
	temp = degree_list
	pos = 0
	for i in xrange(0, len(degree_list)):
		if degree_list[i][1] > x:
			pos = i
			break
	degree_list = degree_list[0:pos]
	degree_list = dict(degree_list)
	degree_key_list = degree_list.keys()
	degree_key_list_bak = degree_key_list
	g.remove_nodes_from(degree_key_list)

def get_degree_dict():
	global g
	global expanded
	degree_dict = nx.degree(g)
	degree_list = sorted(degree_dict.iteritems(), key = lambda asd:asd[1])
	pos = 0
	for i in xrange(0, len(degree_list)):
		if degree_list[i][1] > 0:
			pos = i
			break
	degree_list = degree_list[pos:len(degree_list)]

	degree_dict = dict(degree_list)
	for item in expanded:
		if item in degree_dict:
			degree_dict.pop(item)
	return degree_dict

def get_label_dict(degree_dict):
	global g
	label_dict = nx.get_node_attributes(g, 'label')
	label_dict_bak = label_dict.copy()
	for item in label_dict_bak:
		if item not in degree_dict:
			label_dict.pop(item)
	return label_dict

def get_label_set(label_dict, degree_dict):
	label_set = {}
	for item in label_dict.items():
		if item[1] not in label_set:
			label_set[item[1]] = [(item[0],degree_dict[item[0]])]
		else:
			label_set[item[1]].append((item[0],degree_dict[item[0]]))
	return label_set


def get_ordered_label_list(degree_dict):
	label_list = []
	label_dict = get_label_dict(degree_dict)
	label_set = get_label_set(label_dict, degree_dict)
	#label_set = put_elements_in_label_set(label_set, degree_dict, label_dict)
	label_list = sorted(label_set.items(), key = lambda asd: len(asd[1]), reverse=True)
	for item in label_list:
		item[1].sort(key = lambda asd: asd[1], reverse=True)
	return label_list 


def set_g(uid=""):
	global g
	#xx = os.path.isfile(os.getcwd() + "/grouping/sub_graph_1")
	#zz = os.path
	##yy = 
	#1/0
	graph = None
	if os.path.isfile(os.getcwd() + "/grouping/static/result/" + str(uid) + "_sub_graph_1"):
		graph_file = open(os.getcwd() + "/grouping/static/result/" + str(uid) + "_sub_graph_1")
		graph = pk.load(graph_file)
		graph_file.close()
	g = graph

def get_name(nodes):
	name_dict = {}
	for uid in nodes:
		try:
			user = User.objects.get(uid=str(uid))
			name_dict[uid] = user.name
		except:
			try:
				user = client.get.users__show(uid=int(uid))
				name_dict[uid] = user.name
				User.objects.create(uid=str(user.id), name=user.name, avater=user.profile_image_url)
				users = client.get.friendships__friends__bilateral(uid=int(uid), count=int(200))
				print "getting_name " + str(uid)
				for user in users["users"]:
					if int(user.id) in nodes:
						try:
							User.objects.get(uid=str(user.id))
						except:
							User.objects.create(uid=str(user.id), name=user.name, avater=user.profile_image_url)
			except:
				name_dict[uid] = str(uid)
	return name_dict

def adjust_label_list(label_ordered_list):
	global nodes
	token()
	root = None
	for item in label_ordered_list:
		#print "item:"
		#print item
		if item[0] == -1:
			print item
			root = label_ordered_list.pop(label_ordered_list.index(item))
			label_ordered_list.insert(0, root) 
			break
	label_ordered_list = label_ordered_list[:min(len(label_ordered_list), 6)]
	group_number = 0
	label_list = []

	nodes = []
	for item in label_ordered_list:
		for member in item[1]:
			nodes.append(member[0])

	name_dict = get_name(nodes)

	for item in label_ordered_list:
		item = list(item)
		item[0] = group_number
		group_number += 1
		temp = [(x,nodes.index(x),name_dict[x]) for x,y in item[1]]
		item[1] = temp
		item = tuple(item)
		label_list.append(item)

	#nodes = []
	#for item in label_ordered_list:
		#group_id = item[0]
		#for member in item[1]:
			#nodes.append(member[0])
			#g_json["nodes"].append({'group':group_id,'name':str(nodes.index(member[0]))})
	#for item in g.edges():
		#if (item[0] in nodes) and (item[1] in nodes):
			#g_json["links"].append({'source':nodes.index(item[0]), 'target':nodes.index(item[1])})
	return label_list

def json_g():
	global g
	global expanded
	#set_g()
	degree_dict = get_degree_dict()
	#print len(g.nodes())
	label_ordered_list = get_ordered_label_list(degree_dict)
	label_ordered_list = adjust_label_list(label_ordered_list)
	g_json = {"nodes":[],"links":[]}
	nodes = []
	for item in label_ordered_list:
		group_id = item[0]
		for member in item[1]:
			nodes.append(member[0])
			g_json["nodes"].append({'group':group_id,'name': 's' + str(member[1]) + 's'})
	for item in g.edges():
		if (item[0] in nodes) and (item[1] in nodes):
			g_json["links"].append({'source': (nodes.index(item[0])), 'target': (nodes.index(item[1]))})
			#break
	#g_json["links"].append({'source':item[0], 'target':item[1]})
	return g_json
	

def test_g(uid=""):
	global g
	global expanded
	expanded = []
	set_g(uid)
	#print uid
	degree_dict = get_degree_dict()
	#print 'degree_dict'
	#print degree_dict
	#print len(g.nodes())
	label_ordered_list = get_ordered_label_list(degree_dict)
	#for item in label_ordered_list:
		#print item
		#print len(item[1])
	#print nx.degree_histogram(g)
	#uid = label_ordered_list[0][1][0][0]
	#print uid
	#print "label_ordered_list_1"
	#print label_ordered_list
	draw(g, uid)
	#print "label_ordered_list"
	#print label_ordered_list
	label_ordered_list = adjust_label_list(label_ordered_list)
	uid = label_ordered_list[0][1][0][0]
	#print uid
	#print g[uid]
	#difference = list(set(g.nodes()) - set(subg.nodes()))
	neighbors = g.neighbors(uid)
	return label_ordered_list, neighbors

def main():
	global g
	global expanded
	set_g()
	degree_dict = get_degree_dict()
	print len(g.nodes())
	label_ordered_list = get_ordered_label_list(degree_dict)
	for item in label_ordered_list:
		print item
		print len(item[1])
	print nx.degree_histogram(g)
	draw(g)
	
if __name__ == "__main__":
	main()

