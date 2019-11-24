import getstatistics as gstat
import math
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

class ChampionSelectionModel:

	def __init__(self, summoner, pick_order, role,\
	 mates, champions_stats, n_champions):
		# summoner info
		self.summoner = summoner
		self.pick_order = pick_order
		self.role = role

		# game info
		self.mates = mates
		self.champions_stats = champions_stats
		self.n_champions = n_champions
		self.bans = []
		self.picks = []

		# model
		self.graph = None

	def start(self):
		# 1. Initializing the graph
		self.graph = nx.Graph()
		for cs in self.champions_stats:
			self.graph.add_node(cs.name, reward = 0)

		# 2. Connecting the nodes
		for cs in self.champions_stats:
			for counter in cs.counter:
				self.graph.add_edge(cs.name,counter,weight= -float(cs.counter[counter]))
			for strong in cs.strong:
				self.graph.add_edge(cs.name,strong,weight= float(cs.strong[strong]))

		# 3. Updating the base graph using the match history info
		# from the main summoner
		# a. retriving champion normalized win rate stats
		stats = gstat.summoner_stats('zMoog')#self.summoner)

		# b. updating the node weight with the win rate information
		for champion in stats:
			self.graph.nodes[champion]['reward'] += stats[champion]

		# 4. Updating the base graph using the champion masterie

		return None

	def update_single_ban(self,b):
		self.bans.append(b)
		return None

	def update_bans(self,bans):
		for b in bans:
			self.update_single_ban(b)
		return None

	def predict_bans(self):
		return None

	def update_pick(self):
		return None

	def predict_picks(self):
		return None

	def get_entropy(self):
		kv,P_k = self.degree_distribution(self.graph)
		H = 0
		for p in P_k:
			if(p > 0):
				H = H - p*math.log(p, 2)
		return H

	def get_local_cluster(self):
		vcc = []
		for i in self.graph.nodes():
			vcc.append(nx.clustering(self.graph, i))

		vcc= np.array(vcc)
		return vcc

	def show_local_cluster(self):
		vcc = self.get_local_cluster()
		C_l = pd.DataFrame({'Local Cluster Coefficient': vcc})
		C_l.index = self.graph.nodes()
		C_l.plot.hist()
		plt.show()

	def get_global_cluster(self):
		CC = (nx.transitivity(self.graph)) 
		return CC

	def show_graph(self,custom=True):
		# 1. Plotting the graph
		# a. if you want to plot the standard network, use the bellow line
		if not custom:
			nx.draw_networkx(self.graph)

		# b. else use the custom one
		else:
			pos = nx.spring_layout(self.graph)
			nx.draw_networkx_nodes(self.graph, pos, node_color='r',node_size=700)

			ecounter = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d['weight'] <= 0]
			estrong = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d['weight'] > 0]
			nx.draw_networkx_edges(self.graph, pos, edge_color='g', edgelist=ecounter,width=1)
			nx.draw_networkx_edges(self.graph, pos, edge_color='b', edgelist=estrong,width=1)

			nx.draw_networkx_labels(self.graph, pos, font_size=14, font_family='sans-serif')

			plt.axis('off')
			plt.show()

		return None

	def degree_distribution(self,G):
		vk = dict(G.degree())
		vk = list(vk.values())  # we get only the degree values
		vk = np.array(vk)

		maxk = np.max(vk)
		mink = np.min(vk)
		kvalues= range(0,maxk+1) # possible values of k

		Pk = np.zeros(maxk+1) # P(k)
		for k in vk:
			Pk[k] = Pk[k] + 1
		Pk = Pk/sum(Pk) # the sum of the elements of P(k) must to be equal to one

		return kvalues,Pk

	def show_nodes_degree(self):
		kv, P_k = self.degree_distribution(self.graph)
		plt.bar(kv,P_k)
		plt.xlabel("k", fontsize=20)
		plt.ylabel("P(k)", fontsize=20)
		plt.title("Degree distribution", fontsize=20)
		#plt.grid(True)
		plt.show(True)
		return None