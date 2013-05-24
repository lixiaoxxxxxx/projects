import networkx as nx
import random

part_stable_time = 0
step = 0 

def check_stable(g, same_number):
	global part_stable_time
	global step
	flag = True
	total_number = len(g.nodes())
	for n in g.nodes():
		if g.node[n]['label'] != g.node[n]['pre_label']:
			flag = False
			break
			#return False
	if flag == False and (same_number+0.0)/total_number > 0.9:
		part_stable_time += 1
	step += 1
	print 'step+=1'
	if step >= 250:
		return True
		#dir = os.getcwd()
		#graph_file = open(dir + '/' + "graph", 'w')
		#pk.dump(g, graph_file)
		#graph_file.close()
	#if step == 5001:
		#dir = os.getcwd()
		#graph_file = open(dir + '/' + "graph_2", 'w')
		#pk.dump(g, graph_file)
		#graph_file.close()
		#1/0
	if (flag == True) or (flag == False and part_stable_time > 500):
		return True
	else:
		return False

#def super_check(g):
	#for n in g.nodes():
		#if g.node[n]['label'] != g.node[n]['pre_label']:
			#return False
	#return True


def set_same_number(a, b, number):
	if a == b:
		number += 1
	return number

def lp(g, subg):
	global part_stable_time
	global step
	part_stable_time = 0
	step = 0
	same_number = 0
	label = 0
	for n in subg:
		#if subg.node[n].has_key('label') == False:
		subg.node[n]['label'] = label
		subg.node[n]['next_label'] = None
		subg.node[n]['pre_label'] = None
		g.node[n]['label'] = None
		g.node[n]['next_label'] = None
		g.node[n]['pre_label'] = None
		label += 1
	while check_stable(subg, same_number) == False:
		for n in subg.nodes():
			#print "-----------"
			#print n, ' lable is', g.node[n]['label']
			labelset = {}
			labelset[subg.node[n]['label']] = 1

			for b in subg.neighbors(n):
				if subg.node[b]['label'] in labelset:
					labelset[subg.node[b]['label']] += 1
				else:
					labelset[subg.node[b]['label']] = 1

			label_list = labelset.items()
			random.shuffle(label_list)

			label_list = sorted(label_list, key = lambda asd:asd[1], reverse=True)
			subg.node[n]['next_label'] = label_list[0][0]
		same_number = 0

		for n in subg:
			subg.node[n]['pre_label'] = subg.node[n]['label']
			subg.node[n]['label'] = subg.node[n]['next_label']
			same_number = set_same_number(subg.node[n]['pre_label'], subg.node[n]['label'], same_number)

			g.node[n]['pre_label'] = g.node[n]['label']
			g.node[n]['label'] = subg.node[n]['next_label']
	
	#----------------

	#print nx.get_node_attributes((subg), 'label')
	#print nx.get_node_attributes((g), 'label')
	difference = list(set(g.nodes()) - set(subg.nodes()))
	#print difference
	print "difference"
	for n in difference:
		g.node[n]['label'] = None

	step1 = 0
	for n in difference:
		if step1%1000 == 0:
			print step1
		step1 += 1
		labelset = {}
		temp = None
		for b in g.neighbors(n):
			#print n
			#print b
			if g.node[b]['label'] in labelset:
				temp = g.node[b]['label']
				labelset[g.node[b]['label']] += 1
			else:
				labelset[g.node[b]['label']] = 1

		label_list = labelset.items()
		
		#max_label = max(label_list)
		#print len(label_list)
		if len(label_list) == 0:
			g.remove_node(n)
			difference.remove(n)
		elif len(label_list) == 1:
			g.node[n]['label'] = temp
		else:
			random.shuffle(label_list)
			#print label_list
			label_list = sorted(label_list, key = lambda asd:asd[1], reverse=True)
			g.node[n]['label'] = label_list[0][0]
			
	#print nx.get_node_attributes((g), 'label')
	return g, subg

def main():
	g = nx.Graph()
	g.add_node('a')
	g.add_node('b')
	g.add_node('c')
	g.add_node('d')
	g.add_node('e')
	g.add_node('f')
	g.add_node('g')
	g.add_node('h')
	g.add_edge('a', 'b')
	g.add_edge('a', 'c')
	g.add_edge('a', 'd')
	g.add_edge('b', 'c')
	g.add_edge('b', 'd')
	g.add_edge('c', 'd')
	g.add_edge('c', 'e')
	g.add_edge('d', 'e')
	g.add_edge('e', 'f')
	g.add_edge('e', 'g')
	g.add_edge('e', 'h')
	g.add_edge('f', 'h')
	g.add_edge('f', 'g')
	g.add_edge('g', 'h')
	bg = g.copy()
	bg.add_edge('a', 'z')
	bg.add_edge('b', 'y')
	bg.add_edge('g', 'x')
	lp(bg, g)
if __name__ == "__main__":
	main()
