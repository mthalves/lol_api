import matplotlib.pyplot as plt
import networkx as nx

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
			self.graph.add_node(cs.name)

		# 2. Connecting the nodes
		for cs in self.champions_stats:
			for counter in cs.counter:
				self.graph.add_edge(cs.name,counter,weight= -float(cs.counter[counter]))
			for strong in cs.strong:
				self.graph.add_edge(cs.name,strong,weight= float(cs.strong[strong]))

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

	def show_nodes_degree(self):
		return None

	def show_nodes_entropy(self):
		return None