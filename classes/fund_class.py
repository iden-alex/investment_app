from random import random
import numpy as np


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
        self.fund_stocks = [asset for asset in all_assets if (
            asset.type == 'Strock' and asset.num_in_fund)]
        self.fund_bonds = [asset for asset in all_assets if (
            asset.type == 'Bond' and asset.num_in_fund)]
        self.fund_metalls = [asset for asset in all_assets if (
            asset.type == 'Metall' and asset.num_in_fund)]

        self.total_capital = self.free_capital + \
            np.sum([asset.price * asset.num_in_fund for asset in all_assets])

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
