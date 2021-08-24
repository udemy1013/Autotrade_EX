import threading

import schedule

from main import AutoTrade


class Trading(AutoTrade):

    def demo_threads(self):
        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.ready_trade_demo, args=(num,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

    def quit_threads(self):
        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.quit_driver, args=(num,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

    def real_threads(self):
        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.ready_trade_real, args=(num,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

    def ready_threads(self, high_low):
        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.ready_deal, args=(num, high_low,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

    def enter_threads(self):
        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.enter_deal, args=(num,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

    def change_currency_threads(self, currency):
        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.change_currency, args=(num, currency,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

    def change_span_threads(self, highlow_or_turbo, timespan):

        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.change_trade_span, args=(num, highlow_or_turbo, timespan,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

    def keep_connecting_threads(self):
        threads = []
        for num in range(self.account_num):
            threads.append(threading.Thread(target=self.keep_connecting, args=(num,)))
        for item in threads:
            item.start()
        for item in threads:
            item.join()

