from classes.model_class import Model
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivy.metrics import dp

class DepositWindow(Screen):

    def init_model(self, model):
        self.model = model

    def init_deposit(self, deposit):
        self.deposit = deposit
        self.ids.deposit_name.text = deposit.name

        self.ids.deposit_perc.text = str(deposit.perc)
        self.ids.deposit_time.text = str(deposit.time)
        self.ids.invest.text = str(0)

        free_sum = self.model.fund.free_capital
        self.ids.free_sum.text = str(free_sum)
        
        available_to_invest = max(int(free_sum), 0)
        self.ids.invest.max_value = available_to_invest

    def return_to_main(self):
        self.manager.current = 'main'

    def deposit_invest(self):
        deposit_str = self.ids.invest.text.strip()
        if deposit_str:
            deposit_sum = int(deposit_str)
        else:
            deposit_sum = 0
        if deposit_sum != 0:
            self.model.fund.invest_deposit(self.deposit.name, deposit_sum)
        
        if deposit_sum:
            self.manager.screen2.update_screen()
        self.manager.current = 'main'