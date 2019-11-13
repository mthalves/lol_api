class ChampionStat:

	def __init__(self,name,role,tier,counter,strong):
		self.name = name
		self.role = role
		self.tier = tier
		self.counter = counter
		self.strong = strong

	def show(self):
		print('-----')
		print('|',self.name)
		print('-----')
		print('|',self.role)
		print('|',self.tier)
		print('|',self.counter)
		print('|',self.strong)
		print('-----')