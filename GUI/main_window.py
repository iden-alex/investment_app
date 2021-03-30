
from classes.model_class import Model
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivy.metrics import dp


class MainWindow(Screen):
	'''
	Класс основного окна с выводом информации о фонде, таблицей активов и крактим меню
	'''
	def __init__(self, **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		
	def table_on_row_press(self, instance_table, instance_row):
	    #self.manager.current = 'buy_sell'
		self.update_datatable(self.model)
		pass

	def table_on_check_press(self, instance_table, current_row):
		pass

	def update_datatable(self, cur_model):
		self.data_assets = [(id, x.name, x.type, x.price, x.num_in_fund, x.num_in_market) 
										for id, x in cur_model.market.assets.items()]
		self.ids.table.clear_widgets()
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
		self.model = cur_model
	
	def restart_game(self):
		'''
		Функция, активируемая при нажатии "Начать заново"
		Переводит в стартовое окно, удаляя информацию о имеющихся объектах игры
		'''
		Window.size = (900, 600)
		self.manager.current = "start"
		global cur_model
		cur_model = None
