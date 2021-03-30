from random import random


class Market():
    def __init__(self, volatility):
        self.market_volatility = volatility
        self.assets = {
            0: MarketAsset('Surface', 'Stock', 0, self.market_volatility),
            1: MarketAsset('Tesla', 'Stock', 1, self.market_volatility),
            2: MarketAsset('Alibaba', 'Stock', 2, self.market_volatility),
            3: MarketAsset('BioMed', 'Stock', 3, self.market_volatility),
            4: MarketAsset('JPMorgan', 'Bond', 4, self.market_volatility),
            5: MarketAsset('BOEING', 'Bond', 5, self.market_volatility),
            6: MarketAsset('USA_Bonds', 'Bond', 6, self.market_volatility),
            7: MarketAsset('Russia_Bonds', 'Bond', 7, self.market_volatility),
            8: MarketAsset('China_Bonds', 'Bond', 8, self.market_volatility),
            9: MarketAsset('Gold', 'Metall', 9, self.market_volatility),
            10: MarketAsset('Silver', 'Metall', 10, self.market_volatility),
            11: MarketAsset('Platinum', 'Metall', 11, self.market_volatility),
        }
        self.depostis = []

    def update_assets(self):
        for asset in self.assets.values():
            asset.update_price()

    def buy_asset(self, id, num):
        self.assets[id].buy_to_fund(num)

    def sell_asset(self, id, num):
        self.assets[id].sell_from_fund(num)


class MarketAsset():
    def __init__(self, name, asset_type, i, vol):
        self.dict_market_vol = {'Low': 0.5,
                                'Medium': 1,
                                'High': 3, }
        self.dict_asset_vol = {'Metall': 0.2,
                               'Bond': 0.4,
                               'Stock': 0.9
                               }
        if asset_type not in self.dict_asset_vol:
            print("Incorrect asset type")
        self.name = name
        self.id = i
        self.type = asset_type
        self.asset_volatility = self.dict_asset_vol[self.type] * \
            self.dict_market_vol[vol]
        self.num_in_fund = 0
        self.price = int(100000 * random())
        self.num_in_market = int(100000000/self.price)

    def update_price(self):
        self.price += int(self.asset_volatility * random() *
                          random.choice([1, -1]) * self.price())

    def buy_to_fund(self, num):
        new_num_in_fund = self.num_in_fund + num
        if new_num_in_fund < self.num_in_market:
            self.num_in_fund = new_num_in_fund
        else:
            print(
                f'Это больше на {new_num_in_fund - self.num_in_market}, чем есть таких активов на рынке')

    def sell_from_fund(self, num):
        new_num_in_fund = self.num_in_fund - num
        if new_num_in_fund >= 0:
            self.num_in_fund = new_num_in_fund
        else:
            print(f'Вы можете продать только {self.num_in_fund}')


class Deposit():
    def __init__(self):
        pass
