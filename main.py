from classes.model_class import Model
from GUI.main_window import MainWindow
from GUI.start_window import StartWindow
from GUI.asset_window import AssetWindow
from GUI.deposit_window import DepositWindow
from GUI.history_window import HistoryWindow

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


KIVY_FILE = "./graphic.kv"
cur_model = None


class InvestmentFundApp(MDApp):
    """
    Класс приложения, который запускает всю графику и управляет окнами
    """

    def build(self):
        self.root_widget = Builder.load_file(filename=KIVY_FILE)
        self.title = "Инвестиционный фонд"
        # self.theme_cls.theme_style = 'Dark'
        sm = ScreenManager()
        sm.screen1 = StartWindow(name="start")
        sm.screen2 = MainWindow(name="main")
        sm.screen3 = AssetWindow(name="buy_sell_asset")
        sm.screen4 = DepositWindow(name="change_deposit")
        sm.screen5 = HistoryWindow(name="history")
        sm.add_widget(sm.screen1)
        sm.add_widget(sm.screen2)
        sm.add_widget(sm.screen3)
        sm.add_widget(sm.screen4)
        sm.add_widget(sm.screen5)
        return sm


if __name__ == "__main__":
    InvestmentFundApp().run()
