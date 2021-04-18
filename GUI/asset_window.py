from classes.model_class import Model
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivy.metrics import dp


class AssetWindow(Screen):
    """
    Окно покупки/продажи активов.
    Открывается при нажатии на название актива в таблице активов.
    """

    def set_model(self, model):
        self.model = model

    def init_asset(self, asset):
        self.asset = asset
        self.ids.asset_name.text = asset.name
        self.ids.asset_type.text = asset.type
        asset_price = asset.price
        self.ids.asset_price.text = str(asset_price)
        self.ids.assets_in_fund.text = str(asset.num_in_fund)
        self.ids.buy_asset.text = str(0)
        self.ids.sell_asset.text = str(0)

        free_sum = self.model.fund.free_capital
        self.ids.free_sum.text = str(free_sum)

        available_to_buy = max(int(free_sum / asset_price), 0)
        self.ids.buy_asset.max_value = min(
            available_to_buy, asset.num_in_market - asset.num_in_fund
        )
        self.ids.sell_asset.max_value = asset.num_in_fund

    def return_to_main(self):
        """
        Функция, вызываемая при нажатии кнопки "Вернуться"
        """
        self.manager.current = "main"

    def asset_restructuring(self):
        """
        Функция, вызываемая при нажатии кнопки "Подтвердить и вернуться"(покупка актива)
        """
        purchase_str = self.ids.buy_asset.text.strip()
        sale_str = self.ids.sell_asset.text.strip()
        if purchase_str:
            purchase_num = int(purchase_str)
        else:
            purchase_num = 0

        if sale_str:
            sale_num = int(sale_str)
        else:
            sale_num = 0

        if purchase_num != 0:
            self.model.fund.buy_asset(self.asset.name, purchase_num)

        if sale_num != 0:
            self.model.fund.sell_asset(self.asset.name, sale_num)

        if purchase_num or sale_num:
            self.manager.screen2.update_screen()
        self.manager.current = "main"
