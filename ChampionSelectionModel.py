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

	def start(self):
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

	def show(self):
		return None
