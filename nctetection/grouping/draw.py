# -*- coding: utf-8 -*-
#import unicodedata
#import time
#import string
import os, sys
#import json
#import urllib2
#import re
#import random
import pickle as pk
import networkx as nx
#from weibo import APIClient
#from get_code import *
import matplotlib 
import pylab as plt
import random
#from lp import *

#g = nx.Graph()
#expanded = []

#def set_g(g):
	##global g
	#x = os.path
	#1/0
	#graph = None
	#if os.path.isfile("/grouping/graph"):
		#graph_file = open("/grouping/graph", "r")
		#graph = pk.load(graph_file)
		#graph_file.close()
	#g = graph

def draw(g, uid):
	#global g
	#set_g(g)
	#print len(g.nodes())
	#g = lp(g)
	#print "done"
	p = nx.get_node_attributes(g, 'label')
	plt.figure(figsize=(8, 8))
	nx.draw_networkx(g, pos = nx.layout.spring_layout(g),\
			with_labels = False,
			font_size = 9,
			nodelist = p.keys(),
			width = 0.1,
			node_size = 30,
			vmin = 0,
			vmax = 430,
			node_color = p.values(),
			cmap = plt.cm.Reds_r)
	plt.xlim(-0.05, 1.05)
	plt.ylim(-0.05, 1.05)
	#plt.show()
	plt.savefig('grouping/static/result/' + str(uid) + '_xx.png')

def main():
	draw(g)

if __name__ == "__main__":
	main()

