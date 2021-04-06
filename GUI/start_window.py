
from classes.model_class import Model
from kivy.properties import  NumericProperty
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

RED_COLOUR = (1, 0, 0, 1)

class NumericInput(TextInput):
	'''
	Класс виджета ввода числовых параметров с фильтрацией ввода(ограничение сверху/снизу)
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
			self.ids.input_capital.hint_text_color = RED_COLOUR
			return
		start_capital = int(capital_text)
		game_duration = int(self.ids.input_game_duration.value)
		tax = int(self.ids.input_tax.value)
		volatility = self.ids.input_volatility.text
		cur_model = Model(start_capital, game_duration, tax, volatility, self.manager)
		cur_model.start()
		self.manager.current = "main"
		Window.size = (1280, 960)
		
