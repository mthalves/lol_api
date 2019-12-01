from __future__ import division
import getstatistics as gstat
import math
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import operator
import pandas as pd
import random as rd
import time

from ChampionStat import *
from getGameMates import user

GAMEMATENAME = 0
GAMEMATEROLE = 1

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
		self.stats = None

	def start(self):
		print('1) Building Base Model')
		start_t = time.time()
		# 1. Initializing the graph
		self.graph = nx.Graph()
		for cs in self.champions_stats:
			self.graph.add_node(cs.name, reward= (5.0/float(cs.tier)), visits= 0)

		# 2. Connecting the nodes
		for cs in self.champions_stats:
			for counter in cs.counter:
				self.graph.add_edge(cs.name,counter,weight= -float(cs.counter[counter]))
			for strong in cs.strong:
				self.graph.add_edge(cs.name,strong,weight= float(cs.strong[strong]))

		# 3. Updating the base graph using the match history info
		# from the main summoner
		# a. retriving champion normalized win rate stats
		self.stats = gstat.summoner_stats(self.summoner)
		self.stats = sorted(self.stats.items(), key=operator.itemgetter(1),reverse=True)

		# b. updating the node weight with the win rate information
		for champion in self.stats:
			if champion in self.graph.nodes:
				self.graph.nodes[champion]['reward'] += 10*self.stats[champion]

		# 4. Updating the base graph using the champion masterie
		self.mastery = user(self.summoner)
		self.mastery = self.mastery.Mastery
		max_mastery = max([self.mastery[c] for c in self.mastery])
		for champion in self.mastery:
			if champion in self.graph.nodes:
				self.graph.nodes[champion]['reward'] += 5*(self.mastery[champion]/max_mastery)

		# 5. Updating the base graph using the gamemates statistics
		for gamemate in self.mates:
			stats = gstat.summoner_stats(gamemate[GAMEMATENAME])
			for champion in stats:
				if champion in self.graph.nodes:
					self.graph.nodes[champion]['reward'] += stats[champion]

		# 6. Updating the base graph using role information
		for champion in self.champions_stats:
			if champion.role == self.role:
				self.graph.nodes[champion]['reward'] += 5

		print('Execution in',time.time()-start_t,'sec.')
		return None

	def mean_random_walk(self,pref_champ, counters, start_node,\
							walk_len,max_it=20,pick=True):
		if start_node not in self.graph.nodes:
			return([None,0])

		# 1. Initializing the variables
		champ, values = '', np.zeros(max_it)
		cur_node = start_node
		champ = cur_node
		alt = 1 if pick else -1
		
		# 2. Starting the Random Walk
		for it in range(max_it):
			# a. initializing the values
			if cur_node in pref_champ:
				values[it] += self.graph.nodes[cur_node]['reward']	
			elif cur_node in counters:
				values[it] -= self.graph.nodes[cur_node]['reward']
			elif cur_node in self.stats:
				values[it] += self.stats[cur_node]*self.graph.nodes[cur_node]['reward']		
			else:
				values[it] += alt*self.graph.nodes[cur_node]['reward']	

			# b. walking
			for i in range(walk_len):
				self.graph.nodes[cur_node]['visits'] += 1

				# taking the correct edges to walk
				if pick:
					transitions = self.graph.edges(cur_node)
					transitions = [e for e in transitions]
					transitions = [[e,abs(self.graph.get_edge_data(*e)['weight'])]\
					 for e in transitions if self.graph.get_edge_data(*e)['weight'] > 0]
				else:
					transitions = self.graph.edges(cur_node)
					transitions = [e for e in transitions]
					transitions = [[e,abs(self.graph.get_edge_data(*e)['weight'])]\
					 for e in transitions if self.graph.get_edge_data(*e)['weight'] < 0]

				# performing the random walk
				P = [e[1] for e in transitions]
				P = np.array(P)/sum(P)

				p, cum = rd.uniform(0,1), 0
				for j in range(len(transitions)):
					cum += P[j]
					if cum > p:
						old_node = cur_node
						cur_node = transitions[j][0][1]

						if cur_node in counters:
							values[it] -= alt*(P[j]*self.graph.nodes[cur_node]['reward']\
											+ math.sqrt(2*(math.log(self.graph.nodes[cur_node]['visits']+1)\
												/self.graph.nodes[old_node]['visits'])))
						elif cur_node in pref_champ:
							values[it] += alt*(P[j]*self.graph.nodes[cur_node]['reward']\
											+ math.sqrt(2*(math.log(self.graph.nodes[cur_node]['visits']+1)\
												/self.graph.nodes[old_node]['visits'])))
						elif cur_node in self.stats:
							values[it] += alt*(self.stats[cur_node]*self.graph.nodes[cur_node]['reward']\
											+ math.sqrt(2*(math.log(self.graph.nodes[cur_node]['visits']+1)\
												/self.graph.nodes[old_node]['visits'])))
						break

			cur_node = champ

		# 3. Returning the mean values from walk
		return([champ,np.mean(values)])

	def update_single_ban(self,b):
		if b in self.graph.nodes:
			# i. appending the ban
			self.bans.append(b)

			# ii. replicating the effects over the graph
			transitions = self.graph.edges(b)
			transitions = [e for e in transitions]
			transitions = [[e,abs(self.graph.get_edge_data(*e)['weight'])] for e in transitions]
			for e in transitions:
				if e[1] > 0:
					self.graph.nodes[e[0][1]]['reward'] += 1
				else:
					self.graph.nodes[e[0][1]]['reward'] -= 1

			# iii. removing champion from graph
			self.graph.remove_node(b)
		return None

	def update_bans(self,bans):
		for b in bans:
			self.update_single_ban(b)
		return None

	def predict_bans(self):
		print('2) Predicting Bans')
		start_t = time.time()
		# 1. Getting the summoner prefereble champs
		preferable_champs = []
		for champ in self.stats:
			preferable_champs.append(champ[0])
			if len(preferable_champs) == 20:
				break;

		# 2. Getting these champions counters
		counters = {}
		for champ_name in preferable_champs:
			champ = getChampion(champ_name,self.champions_stats)
			for c in champ.counter:
				if c in counters:
					counters[c] += 1
				else:
					counters[c] = 1

		# 4. Running the bans Random Walk
		result = []
		champions_list = [champ.name for champ in self.champions_stats]
		for champ in champions_list:
			mrw = self.mean_random_walk(\
				pref_champ = preferable_champs,\
				counters = counters,\
				start_node = champ,\
				walk_len = int(len(champions_list)*0.10),\
				max_it = 20,\
				pick=False)
			result.append(mrw)

		# 5. Returning the result bans
		result = sorted(result, key=operator.itemgetter(1), reverse=False)[0:self.n_champions]
		result = [r[0] for r in result]
		print('Execution in',time.time()-start_t,'sec.')
		return(result)

	def update_pick(self,p,my_team):
		if p in self.graph.nodes:
			# i. appending the pick
			self.picks.append(p)

			# ii. replicating the effects over the graph
			transitions = self.graph.edges(p)
			transitions = [e for e in transitions]
			transitions = [[e,abs(self.graph.get_edge_data(*e)['weight'])] for e in transitions]
			for e in transitions:
				if e[1] > 0:
					self.graph.nodes[e[0][1]]['reward'] += 1 if my_team else -1
				else:
					self.graph.nodes[e[0][1]]['reward'] += 1

			# iii. removing champion from graph
			self.graph.remove_node(p)
		return None

	def predict_picks(self,pick_round):
		print('3.'+str(pick_round+1)+') Predicting Picks')
		start_t = time.time()
		# 1. Getting the summoner prefereble champs
		preferable_champs = []
		for champ in self.stats:
			preferable_champs.append(champ[0])
			if len(preferable_champs) == 20:
				break;

		# 2. Getting these champions counters
		counters = {}
		for champ_name in preferable_champs:
			champ = getChampion(champ_name,self.champions_stats)
			for c in champ.counter:
				if c in counters:
					counters[c] += 1
				else:
					counters[c] = 1

		# 4. Running the bans Random Walk
		result = []
		champions_list = [champ.name for champ in self.champions_stats]
		for champ in champions_list:
			mrw = self.mean_random_walk(\
				pref_champ = preferable_champs,\
				counters = counters,\
				start_node = champ,\
				walk_len = int(len(champions_list)*0.10),\
				max_it = 20,\
				pick=True)
			if mrw[0] is not None:
				result.append(mrw)

		# 5. Returning the result bans
		result = sorted(result, key=operator.itemgetter(1), reverse=True)
		result = [r[0] for r in result]

		pick_result = []
		for champ_name in result:
			champ = getChampion(champ_name,self.champions_stats)
			if champ.role.upper() == self.role:
				pick_result.append(champ_name)
				if len(pick_result) == self.n_champions:
					break
		print('Execution in',time.time()-start_t,'sec.')
		return(pick_result)

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

	def plot_local_cluster(self):
		vcc = self.get_local_cluster()
		C_l = pd.DataFrame({'Local Cluster Coefficient': vcc})
		C_l.index = self.graph.nodes()
		C_l.plot.hist(bins=10, alpha=0.8)
		plt.show()

	def get_global_cluster(self):
		CC = (nx.transitivity(self.graph)) 
		return CC

	def plot_graph(self,savename,custom=True):
		fig = plt.figure(1)
		# 1. Plotting the graph
		# a. if you want to plot the standard network, use the bellow line
		if not custom:
			nx.draw_networkx(self.graph)

		# b. else use the custom one
		else:
			pos = nx.spring_layout(self.graph,k=50/math.sqrt(self.graph.order()))
			nx.draw_networkx_nodes(self.graph, pos, node_color=range(len(self.graph.nodes)),\
									cmp=plt.cm.Blues, node_size=500)

			ecounter = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d['weight'] <= 0]
			ecounter_weights = [d['weight'] for (u, v, d) in self.graph.edges(data=True) if d['weight'] <= 0]

			estrong = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d['weight'] > 0]
			estrong_weights = [d['weight'] for (u, v, d) in self.graph.edges(data=True) if d['weight'] > 0]
			
			nx.draw_networkx_edges(self.graph, pos, edge_color=ecounter_weights,\
									 edgelist=ecounter,width=2,edge_cmap=plt.cm.Reds)
			nx.draw_networkx_edges(self.graph, pos, edge_color=estrong_weights,\
									 edgelist=estrong,width=2,edge_cmap=plt.cm.Greens)

			mdf_labels = {}
			for node in self.graph.nodes:
				mdf_labels[node] = node[0]

			nx.draw_networkx_labels(self.graph, pos, labels = mdf_labels, font_size=14, font_family='sans-serif')

			plt.axis('off')
			plt.savefig('./imgs/'+savename, bbox_inches='tight')
			plt.close(fig)

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

	def plot_nodes_degree(self,savename):
		fig = plt.figure(1)
		kv, P_k = self.degree_distribution(self.graph)
		plt.bar(kv,P_k, width=0.80, color='b')
		plt.xlabel("Degree (k)", fontsize=20)
		plt.ylabel("P(k)", fontsize=20)
		plt.title("Degree distribution", fontsize=20)

		plt.savefig('./imgs/'+savename, bbox_inches='tight')
		plt.close(fig)
		return None

	def plot_nodes_visits(self, savename):
		fig = plt.figure(1)
		visits = [[champ,self.graph.nodes[champ]['visits']] for champ in self.graph.nodes]
		sum_visits = sum([node[1] for node in visits])

		visits = [[node[0],node[1]/sum_visits] for node in visits]
		visits = [node for node in visits if node[1] > 0.01]
		ticks = [node[0] for node in visits]
		visits = [node[1] for node in visits]
		pos = range(len(visits))

		plt.barh(pos,visits, align='center', color='b')
		plt.yticks(pos, ticks)

		plt.xlabel("Visit Percentage (%)", fontsize=20)
		plt.title("Visit distribution", fontsize=20)

		plt.savefig('./imgs/'+savename, bbox_inches='tight')
		plt.close(fig)
		return None