from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import ssl

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# TODO 1つのドライバー毎にばらばらのIPアドレスから接続する
class AutoTrade:

    def __init__(self):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['enableVNC'] = True
        capabilities["acceptInsecureCerts"] = True
        # self.username self.password self.enter_money を配列で作り、配列のlengthをドライバーの数にする。

        self.accounts = [["2479.kzk@gmail.com", "k24792323", 1000, "かんくん", "-"],
                         ["iidayuya1994@gmail.com", "iikun1003", 2000, "飯田君", "-"],
                         ["hn22915", "Tkms2580", 1000, "たけまささん", "-"],
                         ["mr.tekitou.0627@icloud.com", "ONOjunya0627", 2000, "オノジュンヤ", "-"],
                         ["takuhiro528@gmail.com", "Takuto2468", 1000, "松岡拓冬", "-"],
                         ["HLMI303528", "Ryou0524", 2000, "山崎凌吾", "-"],
                         ["ayuran011@gmail.com", "110Naruya", 5000, "伊藤成也", "-"],
                         ["boicelf415@gmail.com", "ylhoee415", 1000, "武元姫桃", "-"],
                         ["kei.rsk.tcik@icloud.com", "keisama1025", 5000, "沖田 慧", "-"],
                         ["risa9760204@gmail.com", "risa0204", 1000, "山岡里紗", "-"],
                         ["ont.5258@gmail.com", "11335577a", 5000, "吉澤成美", "-"],
                         ["k.r.hina.hima@gmail.com", "kousuke0621", 1000, "ホリカワコウスケ", "-"],
                         ["yottyjun@gmail.com", "junY461120", 1000, "吉川純子"],
                         ["tv2xq.snsd@gmail.com", "mirina1213", 1000, "重光美莉奈"]]

        self.account_num = len(self.accounts)
        self.isTrading = True

        self.driver = []
        for i in range(self.account_num):
            self.driver.append(webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub', desired_capabilities=capabilities))

        # accounts [username, password, トレード資金]

    # highlowにアクセスしてデモで取引する準備
    def ready_trade_demo(self, i):
        self.driver[i].get("https://trade.highlow.com/")
        WebDriverWait(self.driver[i], 40).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div/div/span/span/a[1]')))
        self.driver[i].find_element_by_xpath('//*[@id="header"]/div/div/div/div/div/span/span/a[1]').click()
        WebDriverWait(self.driver[i], 40).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="account-balance"]/div[2]/div/div[1]/a')))
        self.driver[i].find_element_by_xpath('//*[@id="account-balance"]/div[2]/div/div[1]/a').click()

    def ready_trade_real(self, i):
        # トップページからログインまでの動き
        self.driver[i].get("https://trade.highlow.com/")
        self.driver[i].find_element_by_xpath('//*[@id="header"]/div/div/div/div/div/span/span/a[2]').click()
        self.driver[i].find_element_by_xpath('//*[@id="login-username"]').send_keys(self.accounts[i][0])
        self.driver[i].find_element_by_xpath('//*[@id="login-password"]').send_keys(self.accounts[i][1])
        self.driver[i].find_element_by_xpath(
            '//*[@id="signin-popup"]/div[1]/div/div[2]/div[1]/form/div/div[6]/button').click()
        WebDriverWait(self.driver[i], 40).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="assetsGameTypeZoneRegion"]/ul/li[2]')))
        time.sleep(3)
        self.click_bonus(i)

    def click_bonus(self, i):
        try:
            self.driver[i].find_element_by_xpath('//*[@id="account-balance"]/div[2]/div/div[1]/a').click()

        except ElementNotInteractableException:
            print("this driver has no bonus")

        # 資金を入金していない時のホームにいくまで　※上手く動いていない
        # WebDriverWait(self.driver[i], 20).until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@id="account-balance"]/div[2]/div/div[2]/a')))
        # self.driver[i].find_element_by_xpath('//*[@id="account-balance"]/div[2]/div/div[2]/a').click()
        # self.driver[i].find_element_by_xpath('//*[@id="main-menu"]/div/ul/li[1]/span/a').click()

    def quit_driver(self, i):
        self.driver[i].quit()

    def ready_deal(self, i, high_low):

        if high_low == "high":
            self.driver[i].find_element_by_xpath('//*[@id="up_button"]').click()

        if high_low == "low":
            self.driver[i].find_element_by_xpath('//*[@id="down_button"]').click()

        # エントリー金額を一旦リセットし、登録分を入力
        self.driver[i].find_element_by_xpath('//*[@id="amount"]').clear()
        self.driver[i].find_element_by_xpath('//*[@id="amount"]').send_keys(self.accounts[i][2])

    def enter_deal(self, i):
        self.driver[i].find_element_by_xpath('//*[@id="invest_now_button"]').click()

    # TODO ターボに無い通貨をターボの時に選べないようにする
    def change_currency(self, i, currency):
        self.driver[i].find_element_by_xpath('//*[@id="highlow-asset-filter"]/span[1]').click()
        self.driver[i].find_element_by_xpath('//*[@id="searchBox"]').send_keys(currency)
        time.sleep(3)
        self.driver[i].find_element_by_xpath('//*[@id="assetsFilteredList"]/div').click()

    def keep_connecting(self, i):
            self.driver[i].refresh()
            print("Refreshed")

    def change_trade_span(self, i, highlow_or_turbo, timespan):
        if highlow_or_turbo == "highlow":
            self.driver[i].find_element_by_xpath('//*[@id="assetsGameTypeZoneRegion"]/ul/li[1]').click()

            if timespan == "five":
                self.driver[i].find_element_by_xpath(
                    "/html/body/div[2]/div/div/div/div/div/div[2]/section[3]/div/ul/li/section[1]/div/div/div[1]/div/div/div[2]/div[4]/div/div[1]").click()

            if timespan == "ten":
                self.driver[i].find_element_by_xpath(
                    "/html/body/div[2]/div/div/div/div/div/div[2]/section[3]/div/ul/li/section[1]/div/div/div[1]/div/div/div[2]/div[4]/div/div[2]").click()

            if timespan == "fifteen":
                self.driver[i].find_element_by_xpath(
                    "/html/body/div[2]/div/div/div/div/div/div[2]/section[3]/div/ul/li/section[1]/div/div/div[1]/div/div/div[2]/div[4]/div/div[3]").click()

        elif highlow_or_turbo == "turbo":
            self.driver[i].find_element_by_xpath('//*[@id="assetsGameTypeZoneRegion"]/ul/li[3]').click()

            if timespan == 30:
                self.driver[i].find_element_by_xpath('//*[@id="assetsCategoryFilterZoneRegion"]/div/div[2]').click()

            if timespan == 60:
                self.driver[i].find_element_by_xpath('//*[@id="assetsCategoryFilterZoneRegion"]/div/div[3]').click()

            if timespan == 150:
                self.driver[i].find_element_by_xpath('//*[@id="assetsCategoryFilterZoneRegion"]/div/div[4]').click()

            if timespan == 300:
                self.driver[i].find_element_by_xpath('//*[@id="assetsCategoryFilterZoneRegion"]/div/div[5]').click()

