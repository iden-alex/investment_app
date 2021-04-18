from random import choice
from random import random

START_NUM_FUND_ITEMS = 100
FUND_ITEMS_VOLATILITY = 2


class InvestFund:
    """
    Класс инвестиционного фонда, которым управляет пользователь
    """

    def __init__(self, _market, input_capital, tax, acts_list):
        self.market = _market
        self.actions_list = acts_list
        self.start_capital = input_capital
        self.free_capital = input_capital
        self.total_capital = input_capital
        self.capital_in_deposits = 0
        self.capital_in_assets = 0

        self.income_tax = tax
        self.start_num_items = START_NUM_FUND_ITEMS
        self.total_fund_items = START_NUM_FUND_ITEMS
        self.price_fund_item = self.total_capital / self.total_fund_items
        self.item_profit = 0
        self.assets_profit = 0
        self.deposit_profit = 0

    def update_fund_state(self):
        """
        Обновление капитала фонда
        """
        # активы
        self.capital_in_assets = round(
            sum(
                [
                    asset.price * asset.num_in_fund
                    for _, asset in self.market.assets.items()
                ]
            )
        )
        # депозиты
        self.capital_in_deposits = round(
            sum([deposit.sum_ for deposit in self.market.fund_deposits])
        )
        self.total_capital = (
            self.free_capital + self.capital_in_deposits + self.capital_in_assets
        )

    def buy_asset(self, name, num):
        """
        Покупка активва
        """
        cost = self.market.buy_to_fund(name, num)
        assert 0 <= cost <= self.free_capital
        self.free_capital -= cost
        self.assets_profit -= cost
        self.update_fund_state()

    def sell_asset(self, name, num):
        """
        Продажа актива
        """
        income = self.market.sell_from_fund(name, num)
        self.free_capital += income
        self.assets_profit += income
        self.update_fund_state()

    def fund_items_update(self, old_capital):
        """
        Моделирование покупки/продажи рынком паев фонда
        """
        delta = self.total_capital - old_capital
        if delta > 0:
            fund_efficency = min(delta / old_capital, 1)
        else:
            fund_efficency = max(delta / old_capital, -1)
        self.price_fund_item = round(self.total_capital / self.total_fund_items)
        delta_items = round(
            FUND_ITEMS_VOLATILITY * fund_efficency * random() * self.total_fund_items
        )
        delta_money = delta_items * self.price_fund_item
        self.item_profit += delta_money
        self.free_capital += delta_money
        self.total_capital += delta_money

        self.total_fund_items += delta_items
        self.price_fund_item = round(self.total_capital / self.total_fund_items)

        if delta_items > 0:
            act = f"Приход паев: {delta_items} шт, +{delta_money} у.е."
            self.actions_list.append(act)
        if delta_items < 0:
            act = f"Отток паев: {delta_items} шт, -{delta_money} у.е."
            self.actions_list.append(act)

    def invest_deposit(self, name, sum_):
        """
        Инвестирование в депозит
        """
        assert self.free_capital >= sum_
        self.free_capital -= sum_
        self.deposit_profit -= sum_
        # создание депозита-вложения
        self.market.create_investing_deposit(name, sum_)

    def set_depo_income(self, income):
        """
        Вызывается при окончании срока депозита
        """
        self.free_capital += income
        self.deposit_profit += income

    def set_bond_income(self, income):
        """
        Вызывается при получении выплаты от облигаций
        """
        self.free_capital += income
        self.assets_profit += income
