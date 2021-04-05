from random import random, choice
import numpy as np

#percent of start_capital, is needed to init start price for stocks
MAX_INIT_PRICE = 50000
MAX_ASSET_COST = 100000000
MIN_RANGE_PRICE = 1000
MEAN_BONDS_PERC = 0.03
PERC_IN_PRICE_CONTRIB = 5
BOUND_START_PRICE = 1000

MARKET_VOLATILITY_USER_SET = {  
    'Low': 0.2,
    'Medium': 0.5,
    'High': 1.1, 
 }

ASSETS_VOLATILITY = {   
    'Металл': 0.2,
    'Гос.облигация': 0.03,
    'Акция': 0.8
}

STOCKS_LIST = [
    'Coca-Cola',
    'Tesla',
    'Alibaba',
    'BioMed',
    'ChillUp',
    'Apple',
    'Yandex',
]

BONDS_LIST = [
    'ОФЗ 26230',
    'ОФЗ 29012',
    'ОФЗ 26666',
]

METALLS_LIST = [
    'Gold',
    'Silver',
    'Platinum',
]

DEPOSITS_LIST = [
    ('Депозит 1', 4, 3),
    ('Депозит 2', 12, 8)
]


class Market():
    def __init__(self, volatility, start_capital, acts_list):
        self.market_volatility = volatility
        self.direction = choice([-1, 1])
        self.actions_list = acts_list
        self.direction_period = choice([3, 4, 5])
        # инициализация активов
        self.assets = {name: MarketAsset(name, 'Акция', self.market_volatility, start_capital) for name in STOCKS_LIST}
        self.assets.update(
            {name: MarketAsset(name, 'Гос.облигация', self.market_volatility, start_capital) for name in BONDS_LIST}
            )
        self.assets.update(
            {name: MarketAsset(name, 'Металл', self.market_volatility, start_capital) for name in METALLS_LIST}
            )
        # инициализация депозитов
        self.deposits = {name: Deposit(name, time, perc) for name, perc, time in DEPOSITS_LIST}
        self.fund_deposits = []
        self.invested_deposit_count = 0

    def update_assets(self):
        for asset in self.assets.values():
            asset.update_price(self.direction)

    def buy_to_fund(self, name, num):
        asset = self.assets[name] 
        cost = asset.buy(num)
        act = f'Покупка {asset.name}: кол-во - {num} шт., цена: {asset.price}, потрачено: {cost}'
        self.actions_list.append(act)
        return cost

    def sell_from_fund(self, name, num):
        asset = self.assets[name]
        pay = asset.sell(num)
        act = f'Продажа {asset.name}: кол-во - {num} шт., цена: {asset.price}, получено: {pay}'
        self.actions_list.append(act)
        return pay

    def create_investing_deposit(self, deposit_name, sum):
        base_deposit = self.deposits[deposit_name]
        new_name = f"Вложение {self.invested_deposit_count}"
        self.invested_deposit_count += 1
        new_deposit = Deposit(new_name, 
            base_deposit.time, 
            base_deposit.perc,
            sum,
            base_deposit.time)
        self.fund_deposits.append(new_deposit)
        act = f'Вложение в депозит по: {base_deposit.name}(вклад: {new_deposit.sum}\
                    , срок: {new_deposit.time}, процент: {new_deposit.perc}'
        self.actions_list.append(act)

    def tick_invested_deposits(self):
        for deposit in self.fund_deposits:
            deposit.time_left -= 1
            if deposit.time_left < 1:
                income = int(deposit.sum * (1 + deposit.perc / 100))
                self.fund_deposits.remove(deposit)
                act = f'Начисление депозита по: {deposit.name}(вклад: {deposit.sum}, срок: {deposit.time}, процент: {deposit.perc}, получено: {income})'
                self.actions_list.append(act)
                return income
                
            else:
                return 0
    
    def tick_bonds(self):
        income = round(np.sum(
            [asset.price * asset.num_in_fund * asset.percent / 100 for _, asset in self.assets.items()]
            ))
        self.actions_list.append(f'Начисление выплаты купона по облигациям: +{income}')
        return income

    def update_direction(self, month):
        if month %  self.direction_period == 0:
            self.direction *= -1


class MarketAsset():
    def __init__(self, name, asset_type, vol, start_capital):
        self.dict_market_vol = MARKET_VOLATILITY_USER_SET
        self.dict_asset_vol = ASSETS_VOLATILITY
        if asset_type not in self.dict_asset_vol:
            print("Incorrect asset type")
        self.name = name
        self.type = asset_type
        self.asset_volatility = self.dict_asset_vol[self.type] * \
            self.dict_market_vol[vol]
        self.num_in_fund = 0
        if asset_type == 'Гос.облигация':
            self.percent = MEAN_BONDS_PERC * (1  + 0.5 * choice([-1, 1]) * random())
            self.percent = round(self.percent, 3)
            self.price = BOUND_START_PRICE
        else:
            self.percent = 0
            self.price = int(MAX_INIT_PRICE * random())
        self.num_in_market = int(MAX_ASSET_COST/self.price)

    def update_price(self, market_direction):
        self.price += int(self.asset_volatility * (random() * market_direction - PERC_IN_PRICE_CONTRIB * self.percent) * self.price)

    def buy(self, num):
        new_num_in_fund = self.num_in_fund + num
        assert 0 <= new_num_in_fund < self.num_in_market
        self.num_in_fund = new_num_in_fund
        delta_sum = num * self.price
        return delta_sum
        
    def sell(self, num):
        new_num_in_fund = self.num_in_fund - num
        assert 0 <= new_num_in_fund < self.num_in_market
        self.num_in_fund = new_num_in_fund
        delta_sum = num * self.price
        return delta_sum

class Deposit():
    def __init__(self, name, time, perc, sum=0, time_left=0):
        self.name = name
        self.time = time
        self.perc = perc
        self.sum = sum
        self.time_left = time_left
