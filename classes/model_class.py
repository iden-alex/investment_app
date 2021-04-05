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
		self.month_counter = 1
		self.screen_manager = sm
		self.market = None
		self.fund = None
		self.actions_list = []

	def start(self):
		'''
		Старт моделирования
		'''
		self.market = Market(self.volatility, self.start_capital, self.actions_list)
		self.fund = InvestFund(self.market, self.start_capital, self.tax, self.actions_list)
		self.screen_manager.screen2.init_model(self)
		self.screen_manager.screen3.init_model(self)
		self.screen_manager.screen4.init_model(self)
		self.actions_list.append("Месяц 1")

	def tick(self):
		'''
		Переход к следующему ходу
		'''
		
		if self.month_counter >= self.game_duration:
			return 
		old_capital = self.fund.total_capital
		self.month_counter += 1

		self.market.update_direction(self.month_counter)
		self.market.update_assets()

		income_deposit = self.market.tick_invested_deposits()
		if income_deposit:
			self.fund.get_depo_income(income_deposit)
		
		income_bonds = self.market.tick_bonds()
		if income_bonds:
			self.fund.get_bond_income(income_bonds)

		self.fund.update_fund_state()
		self.fund.fund_items_update(old_capital)
		self.fund.update_fund_state()
		self.actions_list.append(f"Месяц {self.month_counter}")


