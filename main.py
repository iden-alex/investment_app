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

kivy_file = './graphic.kv'
RED_COLOR = (1, 0, 0, 1)

myExperiment = None

class NumericInput(TextInput):
	'''
	Класс виджета ввода капитала, который фильтрует 
	'''
	min_value = NumericProperty()
	max_value = NumericProperty()
	def __init__(self, *args, **kwargs):
		TextInput.__init__(self, *args, **kwargs)
		self.input_filter = 'int'
		self.multiline = False
	def insert_text(self, substring, from_undo=False):
		new_text = self.text + substring
		if substring.isdigit():
			if self.min_value <= int(new_text) <= self.max_value:
				return super(NumericInput, self).insert_text(substring, from_undo=from_undo)
		else:
			return TextInput.insert_text(self, '', from_undo=from_undo)
				
class StartWindow(Screen):
	#start_capital = NumericProperty() 
	#game_duration = ObjectProperty() 
	#tax = ObjectProperty() 
	def start_model(self):
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
	pass

class MainWindow(Screen):
	def __init__(self, **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		self.data_table=MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.5},
							size_hint=(0.9, 0.6),
							check=True,
							rows_num=10,
							column_data=[
                                    ("No.", dp(18)),
                                    ("Food", dp(20)),
                                    ("Calories", dp(20))
                            ],
							row_data=[
                                    ("1", "Burger", "300"),
                                    ("2", "Oats", "200"),
                                    ("3", "Oats", "200"),
                                    ("4", "Oats", "200"),
                                    ("5", "Oats", "200"),
                                    ("6", "Oats", "200"),
                                    ("7", "Oats", "200"),
                                    ("8", "Oats", "200")

                                ]
		)
		self.data_table.bind(on_row_press=self.table_on_row_press)
		self.data_table.bind(on_check_press=self.table_on_check_press)
		self.ids.table.add_widget(self.data_table)
		
	def table_on_row_press(self, instance_table, instance_row):
		pass

	def table_on_check_press(self, instance_table, current_row):
		pass
	
	def tmp(self):
		Window.size = (640, 480)
	pass


class InvestmentFundApp(MDApp):
	def build(self):
		self.root_widget = Builder.load_file(filename=kivy_file)
		self.title = "Инвестиционный фонд"
		#self.theme_cls.theme_style = 'Dark'

		sm = ScreenManager()
		sm.add_widget(StartWindow(name='start'))
		sm.add_widget(MainWindow(name='main'))
		return sm

	def on_row_press(self, instance_table, instance_row):
		print(instance_table, instance_row)

	def on_check_press(self, instance_table, current_row):
		print(instance_table, current_row)

class Game_parametersApp(App):
	def build(self):
		return Experiment()

class Experiment():
	start_capital = 100000
	game_duration = 12
	tax = 0.13
	volatility = 'Низкая'
	def __init__(self, inp_capital = 100000, 
			inp_game_dur = 12, 
			inp_tax = 13, 
			inp_vol = 13):
		self.start_capital = inp_capital
		self.game_duration = inp_game_dur
		self.tax = inp_tax
		self.volatility = inp_vol

	def start():
		pass 

	def tick():
		pass

class InvestFound():
	assets = []
	capital = 0
	pass

class Market():
	pass

class MarketAsset():

	pass

class Stock(MarketAsset):
	pass

class Metall(MarketAsset):
	pass

#облигации
class Bond(MarketAsset):
	pass

class Deposit():
	pass

if __name__ ==  "__main__":
	InvestmentFundApp().run()   