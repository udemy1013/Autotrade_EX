from threads import Trading
import PySimpleGUI as sg
import ssl
import schedule

ssl._create_default_https_context = ssl._create_unverified_context
trading = Trading()
sg.theme("Dark Brown")
header = ['ユーザーネーム', '口座残高', '取引金額', "名前", 'セッションID']
member_list = trading.accounts


# テーブルオブジェクト作成

col1 = [
    [sg.Table(member_list, headings=header, key="table", auto_size_columns=False, col_widths=5)],
    [sg.Button('Start', size=(15, 1)), sg.Button('Quit', size=(15, 1))],
]

col2 = [
    [sg.Text("ターボ", justification="center")],
    [sg.Button('30秒', size=(7, 1), key="turbo30"), sg.Button('1分', size=(7, 1), key="turbo60"),
     sg.Button('3分', size=(7, 1), key="turbo150"), sg.Button('5分', size=(7, 1), key="turbo300")],
    [sg.Text("HighLow", justification="center")],
    [sg.Button('5分', size=(10, 1), key="five"), sg.Button('10分', size=(10, 1), key="ten"),
     sg.Button('15分', size=(10, 1), key="fifteen")],
    [sg.Button('High', size=(15, 1), button_color=("white", "#79B020")),
     sg.Button('Low', size=(15, 1), button_color=("white", "#E54F37"))],
    [sg.Button('今すぐ購入', size=(32, 1), key="enter", button_color=("black", "#FFE462"))],
    [sg.Combo(
        ["AUD/JPY", "AUD/USD", "CAD/JPY", "CHF/JPY", "EUR/AUD", "EUR/GBP", "EUR/JPY", "EUR/USD", "GBP/AUD", "GBP/JPY",
         "GBP/USD", "NZD/JPY", "NZD/USD", "USD/CAD", "USD/CHF", "USD/JPY"], size=(15, 1), key="combo"),
        sg.Button("通貨変更", size=(15, 1), key="change")],
]

layout = [
    [sg.Column(col1, justification="l"), sg.Column(col2, justification="l")]
]

# ウィンドウ作成
window = sg.Window('HighLow オートトレード', layout)

# イベントループ
while True:

    event, values = window.read()  # イベントの読み取り（イベント待ち）

    if event in (None, "Quit"):  # 終了条件（None:クローズボタン）
        trading.quit_threads()
        break

    elif event == "Start":
        # TODO リアルに戻す
        trading.real_threads()
        window["table"].update(values=trading.accounts)

    elif event == "change":
        trading.change_currency_threads(values["combo"])
        print(values["combo"])

    elif event == "turbo30":

        trading.change_span_threads("turbo", 30)

    elif event == "turbo60":
        trading.change_span_threads("turbo", 60)

    elif event == "turbo150":
        trading.change_span_threads("turbo", 150)

    elif event == "turbo300":
        trading.change_span_threads("turbo", 300)

    elif event == "five":
        trading.change_span_threads("highlow", "five")

    elif event == "ten":
        trading.change_span_threads("highlow", "ten")

    elif event == "fifteen":
        trading.change_span_threads("highlow", "fifteen")

    elif event == "High":
        trading.ready_threads("high")

    elif event == "Low":
        trading.ready_threads("low")

    elif event == "enter":
        trading.enter_threads()

window.close()
