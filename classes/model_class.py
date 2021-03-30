from classes.market_class import Market
from classes.fund_class import InvestFund

class Model():
	'''
	Основной класс моделирования
	'''

	def __init__(self, 
				inp_capital, 
				inp_game_dur,
				inp_tax,
				inp_vol,
				sm):
		self.start_capital = inp_capital
		self.game_duration = inp_game_dur
		self.tax = inp_tax
		self.volatility = inp_vol
		self.month_counter = 0
		self.screen_manager = sm
		self.market = None
		self.fund = None

	def start(self):
		'''
		Старт моделирования
		'''
		self.market = Market(self.volatility)
		self.fund = InvestFund(self.market, self.start_capital, self.tax)
		self.screen_manager.screen2.update_datatable(self)

	def tick(self):
		'''
		Изменяет временной счетчик игры
		'''
		if self.month_counter < self.game_duration:
			self.month_counter += 1
			self.market.update_assets()
			self.fund.update_fund_stocks()
			# sm.screen2.update_datatable()
		else:
			print("Game is finished")
