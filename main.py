from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

from kivy.uix.screenmanager import ScreenManager, Screen

class FirstWindow(Screen):
	start_capital = ObjectProperty() 
	game_duration = ObjectProperty() 
	tax = ObjectProperty() 


	def tmp(self):
		Window.size = (1280, 960)

		print(self.start_capital, self.game_duration, self.tax)
	pass

class SecondWindow(Screen):
	def tmp(self):
		Window.size = (640, 480)
	pass

class WindowManager(ScreenManager):
	pass

kv = Builder.load_file('/home/alex/MSU/8_sem/prak/new_windows.kv')

class InvestmentFundApp(App):
	def build(self):
		return kv


class Game_parametersApp(App):
	def build(self):
		return Experiment()

class Experiment():
	start_capital = 100000
	game_duration = 12
	tax = 0.13
	empty_invest_portfolio = True

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