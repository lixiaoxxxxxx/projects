# -*- coding: utf-8 -*-
import unicodedata
import time
import string
import os, sys
import json
import urllib2
import re
import random
import math
import pickle as pk
import networkx as nx
from weibo import APIClient
from get_code_0 import *
from get_code_1 import *
from get_code_2 import *
#from lp import *
from lp_v1 import *

root_uid=1844113285
#root_uid=1794476392
g = nx.Graph()
sub_g = nx.Graph()
expanded = []
x = 1

def token(x): 
	if x % 3 == 0:
		r = client_0.request_access_token(get_code_0())
		client_0.set_access_token(r.access_token, r.expires_in)
	elif x % 3 == 1:
		r = client_1.request_access_token(get_code_1())
		client_1.set_access_token(r.access_token, r.expires_in)
	else:
		r = client_2.request_access_token(get_code_2())
		client_2.set_access_token(r.access_token, r.expires_in)


def get_bilateral(uid):
	#token()
	global root_uid
	global x
	try:
		if x % 3 == 0:
			temp = client_0.get.friendships__friends__bilateral__ids(uid=int(uid), count=int(300))
		elif x % 3 == 1:
			temp = client_1.get.friendships__friends__bilateral__ids(uid=int(uid), count=int(300))
		else:
			temp = client_2.get.friendships__friends__bilateral__ids(uid=int(uid), count=int(300))
	except:
		x = x + 1
		print 'wait 1 wait\n\n'
		token(x)
		if x % 3 == 0:
			temp = client_0.get.friendships__friends__bilateral__ids(uid=int(uid), count=int(300))
		elif x % 3 == 1:
			temp = client_1.get.friendships__friends__bilateral__ids(uid=int(uid), count=int(300))
		else:
			temp = client_2.get.friendships__friends__bilateral__ids(uid=int(uid), count=int(300))
		print 'kakakkakkakkakakkakan\n\n'
	temp = temp['ids']
	if root_uid in temp:
		temp.remove(root_uid)
	#number = min(len(temp), 50)
	#temp = random.sample(temp, number)
	return temp
	pass

def add_to_g(uid, uid_list):
	global g
	global sub_g
	global expanded
	if uid != root_uid:
		g.add_edges_from(zip([uid]*len(uid_list), uid_list))
		for item in uid_list:
			if item in expanded:
				sub_g.add_edge(item, uid)
	else:
		g.add_nodes_from(uid_list)
		g.add_nodes_from(uid_list)

def expand(uid):
	global expanded
	uid_list = get_bilateral(uid)
	add_to_g(uid, uid_list)
	expanded.append(uid)
	print uid
	print len(expanded)
	return uid_list

def get_x_percent_list(percent, uid_list):
	number = len(uid_list) * percent / 100
	if number < 30:
		number = min(len(uid_list), 30)
	slice_list = random.sample(uid_list, number)
	return slice_list

	#print nx.get_node_attributes(lp(g), 'label')

def get_degree_dict():
	global g
	global expanded
	degree_dict = nx.degree(g)
	#print "get_degree_dict:", degree_dict
	#print 'expanded:', expanded
	degree_list = sorted(degree_dict.iteritems(), key = lambda asd:asd[1])

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
	label_list = sorted(label_set.items(), key = lambda asd: len(asd[1]), reverse=True)
	for item in label_list:
		item[1].sort(key = lambda asd: asd[1], reverse=True)
	return label_list 

def get_expand_target_list():
	global g
	global expanded
	degree_dict = get_degree_dict()

	#print 'degree_dict:', degree_dict
	#print '%%%%'
	label_ordered_list = get_ordered_label_list(degree_dict)

	#if len(label_ordered_list)
	slice_list = []
	group_number = min(len(label_ordered_list), 5)
	for item in label_ordered_list[:group_number]:
		#print item[1]
		#temp = int(math.log(len(item[1]), 2))
		#number = int(math.log(len(item[1]), 2))
		#if temp < 1:
			#number = 1
		#number = int(len(item[1]) / 10) + 1
		#print number
		#if number = 0:
			#number = 1
		number = int(math.log(len(item[1]), 2)) + 1
		slice_list += item[1][:number]
	print 'slice_list  group_number================='
	print slice_list
	print group_number
	print '==================='
	slice_list_uid = dict(slice_list).keys()
	#slice_list = random.sample(degree_list.keys(), min(20, len(degree_list)))
	return slice_list_uid

def set_label():
	global g
	for item in g:
		g.node[item]['label'] = item
	pass

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
	#rest_number = len(degree_list) - pos + 1
	#if int(pow(rest_number, 0.618)) < 80:
		#
	#add_number = len(degree_list) - int(pow(rest_number, 0.618))
	#pos += addnumber
	degree_list = degree_list[0:pos]
	degree_list = dict(degree_list)
	degree_key_list = degree_list.keys()
	degree_key_list_bak = degree_key_list
	g.remove_nodes_from(degree_key_list)

def put_root_back(uid, original_list, sub_g):
	for item in original_list:
		if item in sub_g.nodes():
			sub_g.add_edge(int(uid), item)
	sub_g.node[int(uid)]["label"] = -1

def get_graph(uid):
	global expanded
	global original_list
	global g
	global sub_g
	global x
	token(x)
	print "start"
	original_list = expand(uid)
	#original_list_part = get_x_percent_list(20, original_list)
	#print '********'
	#print original_list
	#print original_list_part
	#print '********'
	#print expanded
	#1/0
	for item in original_list:
		expand(item)
	#for i in xrange(0,5):
	while len(expanded) < min(200, len(original_list)*3):
		#set_label()
		#g_bak = g.copy()
		#del_x_degree_node(1)
		g, sub_g = lp(g, sub_g)
		g_bak = g.copy()
		del_x_degree_node(1)
		target_list = []
		target_list = get_expand_target_list()
		if len(target_list) == 0:
			break
		g = g_bak.copy()
		#g = g_bak.copy()
		for target in target_list:
			expand(target)
			#print target
	#del_x_degree_node(1)
	#print "hello"
	g, sub_g = lp(g, sub_g)
	#print "hi"
	#print uid
	#print original_list
	#print sub_g.nodes()
	#print sub_g.edges()
	put_root_back(uid, original_list, sub_g)
	#print uid
	#print sub_g.node[uid]
	#print "what"
	#del_1_degree_node()

def NCdetection(uid):
	global g
	global sub_g
	global root_uid
	global expanded
	global x
	root_uid = int(uid)
	g = nx.Graph()
	sub_g = nx.Graph()
	expanded = []
	if not os.path.isfile(os.getcwd() + "/grouping/static/result/" + str(uid) + "_sub_graph_1"):
		try:
			get_graph(root_uid)
			print "haha"
			dir = os.getcwd()
			graph_file = open(dir + '/grouping/static/result/' + str(root_uid) + "_graph_1", 'w')
			pk.dump(g, graph_file)
			graph_file.close()
			graph_file = open(dir + '/grouping/static/result/' + str(root_uid) + "_sub_graph_1", 'w')
			pk.dump(sub_g, graph_file)
			graph_file.close()
			graph_file = open(dir + '/grouping/static/result/' + "_sub_graph_1", 'w')
			pk.dump(sub_g, graph_file)
			graph_file.close()
		finally:
			print "kaka"
			pass

def main():
	global g
	global sub_g
	global root_uid
	root_uid = int(sys.argv[1])
	#try:
	get_graph(root_uid)
	#finally:
		#print "haha"
		#dir = os.getcwd()
		#graph_file = open(dir + '/result/' + str(root_uid) + "_graph_1", 'w')
		#pk.dump(g, graph_file)
		#graph_file.close()
		#graph_file = open(dir + '/result/' + str(root_uid) + "_sub_graph_1", 'w')
		#pk.dump(sub_g, graph_file)
		#graph_file.close()
		#graph_file = open(dir + '/result/' + "_sub_graph_1", 'w')
		#pk.dump(sub_g, graph_file)
		#graph_file.close()

	#del_x_degree_node(2)
	#g = lp(g)
	#degree_dict = get_degree_dict()
	#label_ordered_list = get_ordered_label_list(degree_dict)
	#for item in label_ordered_list:
		#print item
	
	#print g.nodes()

if __name__ == "__main__":
	main()

