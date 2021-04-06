from classes.model_class import Model
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem

class HistoryWindow(Screen):
    '''
    Окно с выводом истории операций фонда
    '''
    def update_list(self, acts_list):
        '''
        Обновление виджета списка операций
        '''
        self.ids.acts_list.clear_widgets()
        for act in acts_list:
            self.ids.acts_list.add_widget(
                OneLineListItem(text=act)
            )
    
    def return_to_main(self):
        '''
        Функция, вызываемая при нажатии кнопки "Вернуться"
        '''
        self.manager.current = 'main'