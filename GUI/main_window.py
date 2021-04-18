from classes.model_class import Model
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivy.metrics import dp

RED_COLOUR = (1, 0, 0, 1)
GREEN_COLOUR = (109 / 255, 214 / 255, 113 / 255, 1)
GRAY_COLOUR = (128 / 255, 128 / 255, 125 / 255)


class MainWindow(Screen):
    """
    Класс основного окна с выводом информации о фонде, таблицей активов и кратким меню
    """

    def set_model(self, model):
        self.model = model
        self.update_screen()

    def show_delta(self, id, capital_delta):
        """
        Форматирование и вывод строк, показывающих изменение капитала
        """
        capital_delta_perc = round(100 * capital_delta / self.model.start_capital, 2)
        if capital_delta > 0:
            id.color = GREEN_COLOUR
            id.text = f"+{capital_delta}({capital_delta_perc})"
        elif capital_delta == 0:
            id.color = GRAY_COLOUR
            id.text = f"{capital_delta}"
        else:
            id.color = RED_COLOUR
            id.text = f"{capital_delta}({-capital_delta_perc})"

    def update_screen(self, update_assets=True, update_deposits=True):
        """
        Обновление всех атрибутов на экране
        """
        self.ids.month.text = (
            f"Месяц {self.model.month_counter}/{self.model.game_duration}"
        )

        # капитал
        self.model.fund.update_fund_state()
        self.ids.cur_capital.text = str(self.model.fund.total_capital)
        self.ids.free_capital.text = str(self.model.fund.free_capital)

        # изменение капитала в целом
        capital_delta = self.model.fund.total_capital - self.model.fund.start_capital
        self.show_delta(self.ids.delta_capital, capital_delta)

        # активы
        self.ids.in_assets.text = str(self.model.fund.capital_in_assets)
        assets_delta = self.model.fund.assets_profit + self.model.fund.capital_in_assets
        self.show_delta(self.ids.delta_assets, assets_delta)

        # депозиты
        self.ids.in_deposits.text = str(self.model.fund.capital_in_deposits)
        deposits_delta = (
            self.model.fund.deposit_profit + self.model.fund.capital_in_deposits
        )
        self.show_delta(self.ids.delta_deposits, deposits_delta)

        # паи
        self.ids.full_fund_items.text = str(self.model.fund.total_fund_items)
        self.show_delta(self.ids.fund_items_income, self.model.fund.item_profit)

        if update_assets:
            self.set_table_assets()
        if update_deposits:
            self.set_table_deposits()

    def table_asset_on_row_press(self, instance_table, instance_row):
        """
        Функция, активируемая при нажатии на название актива в таблице активов
        """
        asset_name = instance_row.text
        if asset_name in self.model.market.assets:
            asset = self.model.market.assets[asset_name]
            self.manager.screen3.init_asset(asset)
            self.manager.current = "buy_sell_asset"
        else:
            pass

    def table_deposit_on_row_press(self, instance_table, instance_row):
        """
        Функция, активируемая при нажатии на название депозита в таблице депозитов
        """
        deposit_name = instance_row.text
        if deposit_name in self.model.market.deposits:
            deposit = self.model.market.deposits[deposit_name]
            self.manager.screen4.init_deposit(deposit)
            self.manager.current = "change_deposit"
        else:
            pass

    def set_table_assets(self):
        """
        Удаление имеющейся таблицы активов(если есть) и установка новой(с новыми данными)
        Note: kivymd MDDataTable не имеет API изменения данных таблицы, поэтому приходится добавлять/удалять виджеты
        Из-за этого возникает задержка в пару сек между ходами, разработчики пишут, что проблемы есть и в будущем оптимизируют это
        """
        self.ids.table1.clear_widgets()
        data_assets = [
            (name, x.type, x.price, x.num_in_fund, round(100 * x.percent, 1))
            for name, x in self.model.market.assets.items()
        ]
        self.table_asset = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            rows_num=len(data_assets),
            column_data=[
                ("Название", dp(20)),
                ("Тип", dp(20)),
                ("Цена", dp(20)),
                ("Кол-во в фонде", dp(20)),
                ("Выплата, %/мес", dp(20)),
            ],
            row_data=data_assets,
        )
        if self.model.month_counter >= self.model.game_duration - 1:
            self.table_asset.bind(on_row_press=self.empty_func)
        else:
            self.table_asset.bind(on_row_press=self.table_asset_on_row_press)
        self.ids.table1.add_widget(self.table_asset)

    def set_table_deposits(self):
        """
        Аналогично set_table_assets
        """
        self.ids.table2.clear_widgets()
        invested_deposits = [
            (x.name, x.time_, x.perc, x.sum_, x.time_left)
            for x in self.model.market.fund_deposits
        ]
        deposits_to_buy = [
            (name, x.time_, x.perc, x.sum_, x.time_left)
            for name, x in self.model.market.deposits.items()
        ]
        data_deposit = invested_deposits + deposits_to_buy

        self.table_deposit = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            # size_hint=(0.9, 0.6),
            rows_num=len(data_deposit),
            column_data=[
                ("Название", dp(20)),
                ("Срок, мес", dp(20)),
                ("Процент", dp(20)),
                ("Денег вложено", dp(20)),
                ("До выплаты, мес", dp(20)),
            ],
            row_data=data_deposit,
        )
        if self.model.month_counter >= self.model.game_duration - 1:
            self.table_deposit.bind(on_row_press=self.empty_func)
        else:
            self.table_deposit.bind(on_row_press=self.table_deposit_on_row_press)
        self.ids.table2.add_widget(self.table_deposit)

    def restart_game(self):
        """
        Функция, активируемая при нажатии "Начать заново"
        Переводит в стартовое окно, удаляя информацию о имеющихся объектах игры
        """
        Window.size = (900, 600)
        self.manager.current = "start"
        global cur_model
        cur_model = None

    def end_turn(self):
        """
        Функция, вызываемая при нажатии "Закончить ход"
        """

        self.flag_end_game = self.model.tick()
        self.update_screen()
        self.set_table_assets()
        self.set_table_deposits()
        self.ids.month.text = (
            f"Месяц {self.model.month_counter}/{self.model.game_duration}"
        )
        if self.model.month_counter >= self.model.game_duration:
            self.ids.end_game.text = "Игра закончена"
            self.ids.end_game.on_press = self.empty_func_end
            return

    def show_history(self):
        """
        Функция, вызываемая при нажатии "история фонда"
        """
        self.manager.screen5.update_list(self.model.actions_list)
        self.manager.current = "history"

    def empty_func(self, instance_table, instance_row):
        """
        Функция-заглушка для блокировки действий с таблицей
        """
        pass

    def empty_func_end(self):
        """
        Функция-заглушка для блокировки кнопки "Конец хода"
        """
        pass
