from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty

from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from random import random
import numpy as np

kivy_file = './graphic.kv'
RED_COLOR = (1, 0, 0, 1)

myExperiment = None
sm = ScreenManager()

class NumericInput(TextInput):
	'''
	Класс виджета ввода капитала с фильтрацией ввода
	'''

	min_value = NumericProperty()
	max_value = NumericProperty()
	def __init__(self, *args, **kwargs):
		TextInput.__init__(self, *args, **kwargs)
		self.input_filter = 'int'
		self.multiline = False
	def insert_text(self, substring, from_undo=False):
		'''
		Обработка вводимых символов и фильтрация
		'''
		new_text = self.text + substring
		if substring.isdigit():
			if self.min_value <= int(new_text) <= self.max_value:
				return super(NumericInput, self).insert_text(substring, from_undo=from_undo)
		else:
			return TextInput.insert_text(self, '', from_undo=from_undo)
				
class StartWindow(Screen):
	'''
	Класс стартового окна с параметрами ввода
	'''
	
	def start_model(self):
		'''
		Функция, запускаемая после нажатия "Начать игру". 
		Создает объект класса "Эксперимент" и запускает функцию start()
		'''
		capital_text = self.ids.input_capital.text
		if not capital_text.isnumeric():
			self.ids.input_capital.hint_text_color = RED_COLOR
			return
		start_capital = int(capital_text)
		game_duration = int(self.ids.input_game_duration.value)
		tax = int(self.ids.input_tax.value)
		volatility = self.ids.input_volatility.text

		global myExperiment
		myExperiment = Experiment(start_capital, game_duration, tax, volatility)
		self.manager.current = "main"
		Window.size = (1280, 960)
		myExperiment.start()

class MainWindow(Screen):
	'''
	Класс основного окна с выводом информации о фонде, таблицей активов и крактим меню
	'''

	def __init__(self, **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		
	def table_on_row_press(self, instance_table, instance_row):
		self.manager.current = 'buy_sell'
		#self.update_datatable()
		pass

	def table_on_check_press(self, instance_table, current_row):
		pass

	def update_datatable(self):
		self.data_assets = [(id, x.name, x.type, x.price, x.num_in_fund, x.num_in_market) 
										for id, x in myExperiment.market.assets.items()]
		#self.remove_widget(self.data_table)
		self.data_table=MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.5},
							size_hint=(0.9, 0.6),
							rows_num=len(self.data_assets),
							column_data=[
                                    ("id", dp(18)),
                                    ("Name", dp(20)),
                                    ("Type", dp(20)),
									("Price", dp(20)),
									("Number in fund", dp(20)),
									("Number on market", dp(20)),
                            ],
							row_data=self.data_assets
		)
		self.data_table.bind(on_row_press=self.table_on_row_press)
		self.data_table.bind(on_check_press=self.table_on_check_press)
		self.ids.table.add_widget(self.data_table)
		
		pass
	
	def restart_game(self):
		'''
		Функция, активируемая при нажатии "Начать заново"
		Переводит в стартовое окно, удаляя информацию о имеющихся объектах игры
		'''
		Window.size = (900, 600)
		self.manager.current = "start"
		global myExperiment
		myExperiment = None

class InvestmentFundApp(MDApp):
	'''
	Класс приложения, который запускает всю графику и управляет окнами
	'''

	def build(self):
		self.root_widget = Builder.load_file(filename=kivy_file)
		self.title = "Инвестиционный фонд"
		#self.theme_cls.theme_style = 'Dark'
		sm.screen1 = StartWindow(name='start')
		sm.screen2 = MainWindow(name='main')
		sm.screen3 = Screen(name='buy_sell')
		sm.add_widget(sm.screen1)
		sm.add_widget(sm.screen2)
		sm.add_widget(sm.screen3)
		return sm

class Experiment():
	'''
	Класс эксперимента, который запускает моделирование и обновляет состояние
	'''
	def __init__(self, inp_capital, 
			inp_game_dur, 
			inp_tax, 
			inp_vol):
		self.start_capital = inp_capital
		self.game_duration = inp_game_dur
		self.tax = inp_tax
		self.volatility = inp_vol
		self.month_counter = 0
		self.market = None
		self.fund = None

	def start(self):
		'''
		Старт моделирования
		'''
		self.market = Market(self.volatility)
		self.fund = InvestFund(self.market, self.start_capital, self.tax)
		sm.screen2.update_datatable()

	def tick(self):
		'''
		Изменяет временной счетчик игры
		'''
		if self.month_counter < self.game_duration:
			self.month_counter += 1
			self.market.update_assets()
			self.fund.update_fund_stocks()
			sm.screen2.update_datatable()
		else:
			print("Game is finished")

class InvestFund():
	'''
	Класс инвестиционного фонда, которым управляет пользователь
	'''
	def __init__(self, _market, input_capital, tax):
		self.market = _market
		self.start_capital = input_capital
		self.free_capital = input_capital
		self.total_capital = input_capital

		self.income_tax = tax
		self.total_fund_items = 100
		self.price_fund_item = self.total_capital / self.total_fund_items
		self.item_profit = 0

		self.fund_stocks = []
		self.fund_metalls = []
		self.fund_bonds = []
		self.deposits = []

	def update_fund_stocks(self):
		all_assets = self.market.assets
		self.fund_stocks = [asset for asset in all_assets if (asset.type=='Strock' and asset.num_in_fund)]
		self.fund_bonds = [asset for asset in all_assets if (asset.type=='Bond' and asset.num_in_fund)]
		self.fund_metalls = [asset for asset in all_assets if (asset.type=='Metall' and asset.num_in_fund)]
		
		self.total_capital = self.free_capital + np.sum([asset.price * asset.num_in_fund for asset in all_assets])

	def buy_asset(self, id, num):
		pass

	def sell_asset(self, id, num):
		pass

	def items_sale(self):
		self.price_fund_item = int(self.total_capital / self.total_fund_items)
		delta_items = int((random() - 0.5) * self.total_fund_items)
		
		self.item_profit += delta_items * self.price_fund_item
		self.free_capital += delta_items * self.price_fund_item
		self.total_capital += delta_items * self.price_fund_item

		self.total_fund_items += delta_items
		self.price_fund_item = int(self.total_capital / self.total_fund_items)


class Market():
	def __init__(self, volatility):
		self.market_volatility = volatility
		self.assets = {
			0: MarketAsset('Surface', 'Stock', 0, self.market_volatility),
			1: MarketAsset('Tesla', 'Stock', 1, self.market_volatility),
			2: MarketAsset('Alibaba', 'Stock', 2, self.market_volatility),
			3: MarketAsset('BioMed', 'Stock', 3, self.market_volatility),
			4: MarketAsset('JPMorgan', 'Bond', 4, self.market_volatility),
			5: MarketAsset('BOEING', 'Bond', 5, self.market_volatility),
			6: MarketAsset('USA_Bonds', 'Bond', 6, self.market_volatility),
			7: MarketAsset('Russia_Bonds', 'Bond', 7, self.market_volatility),
			8: MarketAsset('China_Bonds', 'Bond', 8, self.market_volatility),
			9: MarketAsset('Gold', 'Metall', 9, self.market_volatility),
			10: MarketAsset('Silver', 'Metall', 10, self.market_volatility),
			11: MarketAsset('Platinum', 'Metall', 11, self.market_volatility),
		}
		self.depostis = []
	
	def update_assets(self):
		for asset in self.assets.values():
			asset.update_price()
	
	def buy_asset(self, id, num):
		self.assets[id].buy_to_fund(num)

	def sell_asset(self, id, num):
		self.assets[id].sell_from_fund(num)
class MarketAsset():
	def __init__(self, name, asset_type, i, vol):
		self.dict_market_vol = {'Low': 0.5,
								'Medium': 1,
								'High': 3,}
		self.dict_asset_vol = { 'Metall': 0.2,
								'Bond': 0.4,
								'Stock': 0.9
							}
		if asset_type not in self.dict_asset_vol:
			print ("Incorrect asset type")
		self.name = name 
		self.id = i
		self.type = asset_type
		self.asset_volatility = self.dict_asset_vol[self.type] * self.dict_market_vol[vol] 
		self.num_in_fund = 0
		self.price = int(100000 * random())
		self.num_in_market = int(100000000/self.price)

	def update_price(self):
		self.price += int(self.asset_volatility * random() * random.choice([1, -1]) * self.price())

	def buy_to_fund(self, num):
		new_num_in_fund = self.num_in_fund + num
		if new_num_in_fund < self.num_in_market:
			self.num_in_fund = new_num_in_fund
		else:
			print(f'Это больше на {new_num_in_fund - self.num_in_market}, чем есть таких активов на рынке')
	
	def sell_from_fund(self, num):
		new_num_in_fund = self.num_in_fund - num
		if new_num_in_fund >= 0:
			self.num_in_fund = new_num_in_fund
		else:
			print(f'Вы можете продать только {self.num_in_fund}')
class Deposit():
	def __init__(self):
		pass

if __name__ ==  "__main__":
	InvestmentFundApp().run()   