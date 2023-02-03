################################################################
################################################################
import os
import re
import sys
import PIL
import json
import time
import uuid
import socket
import random
import hashlib
import sqlite3
import threading
from PIL import Image
from components import resources, icons
################################################################
import components
from datetime import datetime
from collections import Counter
########################################################################

import numpy as np
import pandas as pd
import pandas, requests
###################################################################

import asyncio
import telegram
from telethon import TelegramClient
from telegram.ext import Updater, MessageHandler, CommandHandler
###################################################################

from googleapiclient.discovery import build
from TelegramCrawler import TelegramCrawler
###################################################################

from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer, QThread, pyqtSignal, QFile, QTextStream, QUrlQuery
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QToolTip, QWidget, QPushButton, QLineEdit, QTextEdit, QProgressBar, QMessageBox, QFontComboBox, QFileDialog, QLabel, QComboBox, QGraphicsView, QTableView, QHBoxLayout
################################################################

_DEFAULT_PAGE_SIZE = 1000

## --> GLOBALS
counter = 0
max_value = 10

def usd_jpy():
    # Set the base URL for the API endpoint
    base_url = "https://api.exchangerate-api.com/v4/latest/USD"

    # Make a GET request to the API
    response = requests.get(base_url)

    # Check the status code of the response to make sure it was successful
    if response.status_code == 200:
        # Parse the response data as JSON
        data = response.json()

        # Get the exchange rate for USD/JPY from the response data
        usd_jpy_rate = data['rates']['JPY']

        # Return the currency pair and exchange rate as a tuple
        return ("USD/JPY", usd_jpy_rate)
    else:
        # If the request was not successful, return None
        return None

# Get the currency pair and exchange rate
currency_pair, exchange_rate = usd_jpy()
usd_pair = currency_pair
usd_rate = exchange_rate

def eur_usd():
    # Set the base URL for the API endpoint
    base_url = "https://api.exchangerate-api.com/v4/latest/USD"

    # Make a GET request to the API
    response = requests.get(base_url)

    # Check the status code of the response to make sure it was successful
    if response.status_code == 200:
        # Parse the response data as JSON
        data = response.json()

        # Get the exchange rate for EUR/USD from the response data
        eur_usd_rate = data['rates']['EUR']

        # Return the currency pair and exchange rate as a tuple
        return ("EUR/USD", eur_usd_rate)
    else:
        # If the request was not successful, return None
        return None

# Get the currency pair and exchange rate
currency_pair, exchange_rate = eur_usd()
eur_pair = currency_pair
eur_rate = exchange_rate

def usd_cad():
    # Set the base URL for the API endpoint
    base_url = "https://api.exchangerate-api.com/v4/latest/USD"

    # Make a GET request to the API
    response = requests.get(base_url)

    # Check the status code of the response to make sure it was successful
    if response.status_code == 200:
        # Parse the response data as JSON
        data = response.json()

        # Get the exchange rate for USD/JPY from the response data
        usd_cad_rate = data['rates']['CAD']

        # Return the currency pair and exchange rate as a tuple
        return ("USD/CAD", usd_cad_rate)
    else:
        # If the request was not successful, return None
        return None

# Get the currency pair and exchange rate
currency_pair, exchange_rate = usd_cad()
cad_pair = currency_pair
cad_rate = exchange_rate

def gbp_usd():
    # Set the base URL for the API endpoint
    base_url = "https://api.exchangerate-api.com/v4/latest/USD"

    # Make a GET request to the API
    response = requests.get(base_url)

    # Check the status code of the response to make sure it was successful
    if response.status_code == 200:
        # Parse the response data as JSON
        data = response.json()

        # Get the exchange rate for USD/JPY from the response data
        gbp_usd_rate = data['rates']['GBP']

        # Return the currency pair and exchange rate as a tuple
        return ("GBP/USD", gbp_usd_rate)
    else:
        # If the request was not successful, return None
        return None

# Get the currency pair and exchange rate
currency_pair, exchange_rate = gbp_usd()
gbp_pair = currency_pair
gbp_rate = exchange_rate

def get_trading_pairs():
    # Set the base URL for the API endpoint
    base_url = "https://api.exchangerate-api.com/v4/latest/USD"

    # Make a GET request to the API
    response = requests.get(base_url)

    # Check the status code of the response to make sure it was successful
    if response.status_code == 200:
        # Parse the response data as JSON
        data = response.json()

        # Get the list of available trading pairs
        trading_pairs = ["USD/" + currency for currency in data['rates'].keys()] + ["EUR/" + currency for currency in data['rates'].keys()]

        # Return the list of trading pairs
        return trading_pairs
    else:
        # If the request was not successful, return None
        return None

# Get the list of trading pairs
trading_pairs = get_trading_pairs()

class TelegramCrawlerThread(QThread):
    signal = pyqtSignal(str, str, str, str)
    def __init__(self, selected_pair):
        QThread.__init__(self)
        self.selected_pair = selected_pair

    def run(self):
        self.telegram_crawler = TelegramCrawler()
        self.telegram_crawler.init(self.selected_pair)
        signal, currency, entry, time = self.telegram_crawler.get_result()
        self.signal.emit(signal, currency, entry, time)

class MyThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(str)
    reset_signal = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.counter = None

    def run(self):
        while self.counter > 0:
            hours = self.counter // 3600
            minutes = (self.counter % 3600) // 60
            seconds = self.counter % 60
            display_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.update_signal.emit(display_text)
            QtCore.QThread.sleep(1)
            self.counter -= 1

        # emit reset signal when counter reaches 0
        self.reset_signal.emit()

class headerThread(QtCore.QThread):
    update_header_function = QtCore.pyqtSignal(float, float, float, float)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            listNumber = random.uniform(0.75, 0.95)
            updatePriceFunction = round(int(listNumber*100), 3)
            updatePriceFunction_2 = round(int(listNumber*100), 3)
            updatePriceFunction_3 = round(int(listNumber*100), 3)
            updatePriceFunction_4 = round(int(listNumber*100), 3)

            self.update_header_function.emit(updatePriceFunction, updatePriceFunction_2, updatePriceFunction_3, updatePriceFunction_4)
            self.sleep(2)

class ApplicationScreen(QMainWindow):
    def __init__(self):
        super(ApplicationScreen, self).__init__()
        loadUi("components/binary.ui", self)
        self.telegram_crawler = TelegramCrawler()
        self.check_saved_login()

        # Start headerThread
        self.headerThread = headerThread()
        self.headerThread.update_header_function.connect(self.update_header)
        self.headerThread.start()
        ########################################################################

        comboTimes = ["1 mins", "2 mins", "3 mins", "4 mins", "5 mins", "10 mins", "15 mins", "30 mins"]
        self.combo_2 = self.findChild(QComboBox, "comboTimer")
        self.combo_2.addItems(comboTimes)
        self.combo_2.setCurrentText("Trading Time")

        self.combo_2.currentTextChanged.connect(self.combo_selection_changed)
        self.my_thread = MyThread()
        self.my_thread.update_signal.connect(self.update_progress_bar)
        self.my_thread.reset_signal.connect(self.reset)

        self.passwordfield.setEchoMode(QLineEdit.Password)
        self.adminPassword.setEchoMode(QLineEdit.Password)
        self.passwordfield_2.setEchoMode(QLineEdit.Password)
        self.confirmpassword.setEchoMode(QLineEdit.Password)

        self.askTag.setText(usd_pair)
        self.quoteTag.setText(str(usd_rate))
        self.askTag_2.setText(gbp_pair)
        self.quoteTag_2.setText(str(gbp_rate))
        self.askTag_3.setText(eur_pair)
        self.quoteTag_3.setText(str(eur_rate))
        self.askTag_4.setText(cad_pair)
        self.quoteTag_4.setText(str(cad_rate))

        self.askTag.hide()
        self.quoteTag.hide()
        self.askTag_2.hide()
        self.quoteTag_2.hide()
        self.askTag_3.hide()
        self.quoteTag_3.hide()
        self.askTag_4.hide()
        self.quoteTag_4.hide()

        QtCore.QTimer.singleShot(1000, lambda: self.askTag.show())
        QtCore.QTimer.singleShot(3000, lambda: self.quoteTag.show())
        QtCore.QTimer.singleShot(5000, lambda: self.askTag_2.show())
        QtCore.QTimer.singleShot(7000, lambda: self.quoteTag_2.show())
        QtCore.QTimer.singleShot(9000, lambda: self.askTag_3.show())
        QtCore.QTimer.singleShot(11000, lambda: self.quoteTag_3.show())
        QtCore.QTimer.singleShot(13000, lambda: self.askTag_4.show())
        QtCore.QTimer.singleShot(15000, lambda: self.quoteTag_4.show())
        QtCore.QTimer.singleShot(20000, lambda: self.askTag.setText("EUR/USD"))
        QtCore.QTimer.singleShot(24000, lambda: self.quoteTag.setText("AUD/USD"))
        QtCore.QTimer.singleShot(28000, lambda: self.askTag_2.setText("USD/JPY"))
        QtCore.QTimer.singleShot(32000, lambda: self.quoteTag_2.setText("GBP/USD"))
        QtCore.QTimer.singleShot(36000, lambda: self.askTag_3.setText("USD/CHF"))
        QtCore.QTimer.singleShot(40000, lambda: self.quoteTag_3.setText("USD/CAD"))
        QtCore.QTimer.singleShot(44000, lambda: self.askTag_4.setText("NZD/USD"))
        QtCore.QTimer.singleShot(48000, lambda: self.quoteTag_4.setText("AUD/CAD"))
        QtCore.QTimer.singleShot(52000, lambda: self.askTag.setText("AUD/CHF"))
        QtCore.QTimer.singleShot(56000, lambda: self.quoteTag.setText("AUD/JPY"))
        QtCore.QTimer.singleShot(60000, lambda: self.askTag_2.setText("AUD/NZD"))
        QtCore.QTimer.singleShot(64000, lambda: self.quoteTag_2.setText("CAD/CHF"))
        QtCore.QTimer.singleShot(68000, lambda: self.askTag_3.setText("CAD/JPY"))
        QtCore.QTimer.singleShot(72000, lambda: self.quoteTag_3.setText("CHF/JPY"))
        QtCore.QTimer.singleShot(76000, lambda: self.askTag_4.setText("EUR/AUD"))
        QtCore.QTimer.singleShot(80000, lambda: self.quoteTag_4.setText("EUR/CAD"))
        QtCore.QTimer.singleShot(84000, lambda: self.quoteTag_2.setText("EUR/CHF"))
        QtCore.QTimer.singleShot(88000, lambda: self.askTag_3.setText("EUR/GBP"))
        QtCore.QTimer.singleShot(92000, lambda: self.quoteTag_3.setText("EUR/JPY"))
        QtCore.QTimer.singleShot(96000, lambda: self.askTag_4.setText("EUR/NZD"))
        QtCore.QTimer.singleShot(100000, lambda: self.quoteTag_4.setText("GBP/AUD"))
        QtCore.QTimer.singleShot(104000, lambda: self.quoteTag_2.setText("GBP/CAD"))
        QtCore.QTimer.singleShot(108000, lambda: self.askTag_3.setText("GBP/CHF"))
        QtCore.QTimer.singleShot(112000, lambda: self.quoteTag_3.setText("GBP/JPY"))
        QtCore.QTimer.singleShot(116000, lambda: self.askTag_4.setText("GBP/NZD"))
        QtCore.QTimer.singleShot(120000, lambda: self.quoteTag_4.setText("NZD/CAD"))
        QtCore.QTimer.singleShot(124000, lambda: self.quoteTag_2.setText("NZD/CHF"))
        QtCore.QTimer.singleShot(128000, lambda: self.askTag_3.setText("NZD/JPY"))
        QtCore.QTimer.singleShot(132000, lambda: self.quoteTag_3.setText("XAU/USD"))
        QtCore.QTimer.singleShot(136000, lambda: self.askTag.setText("EUR/USD"))
        QtCore.QTimer.singleShot(140000, lambda: self.quoteTag.setText("AUD/USD"))
        QtCore.QTimer.singleShot(144000, lambda: self.askTag_2.setText("USD/JPY"))
        QtCore.QTimer.singleShot(148000, lambda: self.quoteTag_2.setText("GBP/USD"))
        QtCore.QTimer.singleShot(152000, lambda: self.askTag_3.setText("USD/CHF"))
        QtCore.QTimer.singleShot(156000, lambda: self.quoteTag_3.setText("USD/CAD"))
        QtCore.QTimer.singleShot(160000, lambda: self.askTag_4.setText("NZD/USD"))
        QtCore.QTimer.singleShot(164000, lambda: self.quoteTag_4.setText("AUD/CAD"))
        QtCore.QTimer.singleShot(168000, lambda: self.askTag.setText("AUD/CHF"))
        QtCore.QTimer.singleShot(172000, lambda: self.quoteTag.setText("AUD/JPY"))
        QtCore.QTimer.singleShot(176000, lambda: self.askTag_2.setText("AUD/NZD"))
        QtCore.QTimer.singleShot(180000, lambda: self.quoteTag_2.setText("CAD/CHF"))
        QtCore.QTimer.singleShot(184000, lambda: self.askTag_3.setText("CAD/JPY"))
        QtCore.QTimer.singleShot(188000, lambda: self.quoteTag_3.setText("CHF/JPY"))
        QtCore.QTimer.singleShot(192000, lambda: self.askTag_4.setText("EUR/AUD"))
        QtCore.QTimer.singleShot(196000, lambda: self.quoteTag_4.setText("EUR/CAD"))
        QtCore.QTimer.singleShot(200000, lambda: self.quoteTag_2.setText("EUR/CHF"))
        QtCore.QTimer.singleShot(204000, lambda: self.askTag_3.setText("EUR/GBP"))
        QtCore.QTimer.singleShot(208000, lambda: self.quoteTag_3.setText("EUR/JPY"))
        QtCore.QTimer.singleShot(212000, lambda: self.askTag_4.setText("EUR/NZD"))
        QtCore.QTimer.singleShot(216000, lambda: self.quoteTag_4.setText("GBP/AUD"))
        QtCore.QTimer.singleShot(220000, lambda: self.quoteTag_2.setText("GBP/CAD"))
        QtCore.QTimer.singleShot(224000, lambda: self.askTag_3.setText("GBP/CHF"))
        QtCore.QTimer.singleShot(230000, lambda: self.quoteTag_3.setText("GBP/JPY"))
        QtCore.QTimer.singleShot(234000, lambda: self.askTag_4.setText("GBP/NZD"))
        QtCore.QTimer.singleShot(238000, lambda: self.quoteTag_4.setText("NZD/CAD"))
        QtCore.QTimer.singleShot(242000, lambda: self.quoteTag_2.setText("NZD/CHF"))
        QtCore.QTimer.singleShot(246000, lambda: self.askTag_3.setText("NZD/JPY"))
        QtCore.QTimer.singleShot(250000, lambda: self.quoteTag_3.setText("XAU/USD"))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(60)
        self.description.setText("FXsignalspot")
        QtCore.QTimer.singleShot(2000, lambda: self.description.setText("<strong>Welcome</strong>&nbsp;&nbsp;to FXsignalspot Binary Trading"))
        QtCore.QTimer.singleShot(3000, lambda: self.description.setText("<strong>Loading...</strong>&nbsp;&nbsp;&nbsp;Don't forget to check us out at https://www.fxsignalspot.com"))
        QtCore.QTimer.singleShot(4000, lambda: self.description.setText("Check us out at https://www.fxsignalspot.com"))
        QtCore.QTimer.singleShot(5000, lambda: self.description.setText("Welcome to Binary Trading with FXsignalspot"))

        self.load.setText(" ")
        QtCore.QTimer.singleShot(1100, lambda: self.load.setText("Loading"))
        QtCore.QTimer.singleShot(1600, lambda: self.load.setText("Loading."))
        QtCore.QTimer.singleShot(2100, lambda: self.load.setText("Loading.."))
        QtCore.QTimer.singleShot(2600, lambda: self.load.setText("Loading..."))
        QtCore.QTimer.singleShot(3100, lambda: self.load.setText("Loading"))
        QtCore.QTimer.singleShot(3600, lambda: self.load.setText("Loading."))
        QtCore.QTimer.singleShot(4100, lambda: self.load.setText("Loading.."))
        QtCore.QTimer.singleShot(4600, lambda: self.load.setText("Loading..."))
        QtCore.QTimer.singleShot(5100, lambda: self.load.setText("Loading"))
        QtCore.QTimer.singleShot(5600, lambda: self.load.setText(" "))

        self.show()

        ########################################################################
        # Set QLabel Widgets
        ########################################################################

        self.updateLabel.setText("EUR/USD")
        self.updateLabel_6.setText("AUD/NZD")
        self.updateLabel_2.setText("USD/JPY")
        self.updateLabel_7.setText("CAD/JPY")
        self.updateLabel_3.setText("NZD/CHF")
        self.updateLabel_8.setText("NZD/CHF")
        self.updateLabel_4.setText("GBP/CAD")
        self.updateLabel_9.setText("CHF/JPY")

        ########################################################################
        ########################################################################

        # Get the stacked widget page named telegramTrends
        stacked_widget = self.telegramTrends

        # Create a WebEngineView widget
        web_view = QWebEngineView()

        # Set the HTML of the WebEngineView widget to an iframe that embeds the website
        web_view.setHtml(f'<iframe width="100%" height="100%" src="https://fxsignalspot.com/" frameborder="0"></iframe>')

        # Add the WebEngineView widget to the layout of the page widget
        stacked_widget.layout().addWidget(web_view)

        ########################################################################

        # Get the stacked widget page named telegramPage
        stacked_widget = self.telegramPage

        # Create a WebEngineView widget and set the URL to the Telegram channel
        web_view = QWebEngineView()
        web_view.setUrl(QUrl("https://t.me/fxsignalspot"))

        # Add the WebEngineView widget to the layout of the page widget
        stacked_widget.layout().addWidget(web_view)

        ########################################################################
        ########################################################################
        stacked_widget = self.subscriptionPage        
        web_view = QWebEngineView()
        web_view.setHtml('''
            <html>
                <head>
                    
                </head>
                <body>
                    <div class="PyQt_webview">
                        <div class="PyQt_header">
                            <h1>Welcome to our Subscription Page! Choose a plan that suits your needs.</h1>
                            <p>Thank you for considering our Subscription Plans. We offer three unique plans, each designed to cater to your specific needs and requirements.</p>
                        </div>

                        <div class="PyQt_webview_container flex_box">
                            <div class="PyQt_webview_box column">
                                <div class="PyQt_webview_header">
                                    <h2>Basic Subscription</h2>
                                </div>

                                <div class="PyQt_webview_content">
                                    <p>Access to all basic features</p>
                                    <p>Limited support</p>
                                    <p>Monthly cost: Free</p>
                                </div>

                                <div class="PyQt_webview_Btn">
                                    <a href="#">Subscribe Here</a>
                                </div>
                            </div>

                            <div class="PyQt_webview_box column">
                                <div class="PyQt_webview_header">
                                    <h2>Premium Subscription</h2>
                                </div>

                                <div class="PyQt_webview_content">
                                    <p>Access to all basic and premium features</p>
                                    <p>Priority support</p>
                                    <p>Monthly cost: $44.00</p>
                                </div>

                                <div class="PyQt_webview_Btn">
                                    <a href="#">Subscribe Here</a>
                                </div>
                            </div>

                            <div class="PyQt_webview_box column">
                                <div class="PyQt_webview_header">
                                    <h2>Ultimate Subscription</h2>
                                </div>

                                <div class="PyQt_webview_content">
                                    <p>Access to all basic, premium, and ultimate features</p>
                                    <p>24/7 support</p>
                                    <p>Monthly cost: $107.00</p>
                                </div>

                                <div class="PyQt_webview_Btn">
                                    <a href="#">Subscribe Here</a>
                                </div>
                            </div>
                        </div>

                        <div class="PyQt_footer">
                            <p>Should you require any assistance in selecting a plan that suits your needs, please do not hesitate to reach out to us. Our customer support team is always available to assist you.</p>
                        </div>
                    </div>

                    <style>
                        .PyQt_webview{
                            justify-content: center;
                            align-content: center;
                            margin: auto;
                            padding: 2%;
                        }

                        .PyQt_webview_container{
                            justify-content: center;
                            align-content: center;
                            margin: auto;
                        }

                        .flex_box{
                            display: grid;
                            grid-template-columns: repeat(auto-fit, minmax(300px, auto));
                            justify-content: center;
                            align-items: center;
                            margin: auto;
                            gap: 1.8rem;
                            padding: 2% 4%;
                        }

                        .PyQt_webview_box{
                            justify-content: center;
                            align-items: flex-start;
                            text-align: center;
                            display: flex;
                            flex-direction: row;
                            width: 100%;
                            height: auto;
                            padding: 10px;
                            margin: auto;
                            box-shadow: 0 5px 25px rgb(1 1 1 / 20%);
                            background-color: 0 5px 25px rgb(5 5 5 / 60%);
                        }

                        .PyQt_header{
                            justify-content: center;
                            align-content: center;
                            margin: auto;
                            text-align: center;
                            width: 80%;
                        }

                        .PyQt_header h1{
                            font-size: 1.4em;
                            font-weight: 700;
                            color: #000000;
                        }

                        .PyQt_header p{
                            font-size: 0.85em;
                            font-weight: 400;
                            color: #444444;
                        }

                        .PyQt_webview_header{
                            justify-content: center;
                            align-content: center;
                            margin: auto;
                            text-align: center;
                        }

                        .PyQt_webview_header h2{
                            font-size: 1em;
                            font-weight: 700;
                            color: #000000;
                        }

                        .PyQt_webview_header p{
                            font-size: 0.75em;
                            font-weight: 400;
                            color: #444444;
                        }

                        .PyQt_webview_content{
                            justify-content: center;
                            align-content: center;
                            margin: auto;
                            text-align: center;
                        }

                        .PyQt_webview_content p{
                            font-size: 0.75em;
                            font-weight: 400;
                            color: #444444;
                        }

                        .column{
                            justify-content: center;
                            align-content: center;
                            text-align: center;
                            margin: auto;
                            display: flex;
                            flex-direction: column;
                            text-align: center;
                        }

                        .PyQt_webview_Btn{
                            justify-content: center;
                            align-content: center;
                            margin: auto;
                            text-align: center;
                        }

                        .PyQt_webview_Btn a{
                            text-decoration: none;
                            font-size: 0.75em;
                            font-weight: 400;
                            color: #444444;
                            padding: 5px 10px;
                            border-radius: 4px;
                            background: #888888;
                        }

                        .PyQt_webview_Btn a:hover{
                            color: #888888;
                            background: #444444;
                        }

                        .PyQt_footer{
                            justify-content: center;
                            align-content: center;
                            margin: auto;
                            text-align: center;
                            width: 80%;
                        }
                        
                        .PyQt_footer p{
                            text-align: center;
                            font-size: 0.85em;
                            font-weight: 400;
                            color: #444444;
                        }
                        
                    </style>
                </body>
            </html>
        ''')
        stacked_widget.layout().addWidget(web_view)
        ########################################################################
        
        self.telegramBtn_2.clicked.connect(self.showTelegramChannel)
        self.closeChannelBtn_2.clicked.connect(self.closeChannel)
        self.brokerBtn_2.clicked.connect(self.trendingsFunc)
        self.signalBtn_2.clicked.connect(self.trendings)
        self.update_prices.clicked.connect(self.trendings)
        self.telegramBtn.clicked.connect(self.showTelegramChannel)
        self.notificationBtn.clicked.connect(self.showNotification)
        self.hideNotificationBtn.clicked.connect(self.hideNotification)
        self.closeChannelBtn.clicked.connect(self.closeChannel)
        self.expandBtn.clicked.connect(self.expand)
        self.restoreBtn.clicked.connect(self.restore)
        self.openAccBtn.clicked.connect(self.openAcc)
        self.closeAccBtn.clicked.connect(self.closeAcc)
        self.showBtn.clicked.connect(self.showMenu)
        self.hideBtn.clicked.connect(self.hideMenu)
        self.proceedBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        self.trendBtn.clicked.connect(self.subscriptionPageFunction)
        self.trendBtn_2.clicked.connect(self.subscriptionPageFunction)
        self.infoBtn.clicked.connect(self.gotoinfopage)
        self.infoBtn_2.clicked.connect(self.gotoinfopage)
        self.helpBtn.clicked.connect(self.gotohelppage)
        self.helpBtn_2.clicked.connect(self.gotohelppage)
        self.loginBtnSubmit.clicked.connect(self.loginfunction)
        self.signUpBtnSubmit.clicked.connect(self.signupfunction)
        self.goToLogInPage.clicked.connect(self.login_Form)
        self.logInBtn.clicked.connect(self.login_Form)
        self.forgetBtn.clicked.connect(self.sign_Up_Form)
        self.signUpBtn.clicked.connect(self.sign_Up_Form)
        self.lightMode.clicked.connect(self.light)
        self.darkMode.clicked.connect(self.black)
        self.brokerBtn.clicked.connect(self.trendingsFunc)
        self.homeBtn.clicked.connect(self.homeContent)
        self.signalBtn.clicked.connect(self.trendings)
        self.showAdsBtn.clicked.connect(self.showAds)
        self.hideAdsBtn.clicked.connect(self.hideAds)
        self.logout.clicked.connect(self.logoutFunction)
        self.settingBtn_2.clicked.connect(self.adminFunction)
        self.settingBtn.clicked.connect(self.adminFunction)
        self.adminLogin.clicked.connect(self.adminLoginFunction)
        self.saveYoutube.clicked.connect(self.saveYoutubeFunction)

    def adminFunction(self):
        self.adminYoutube.hide()
        self.saveYoutube.hide()
        self.youtubeName.hide()
        self.User_form.show()
        self.signUpForm.hide()
        self.loginForm.hide()
        self.trendpage.hide()
        self.bodyContent.hide()

    def set_font_on_widgets(self):
        # Step 1: Download the font file and store it in the project directory
        font_file = QFile("components/fonts/Poppins-medium.ttf")
        font_file.open(QFile.ReadOnly)

        # Step 2: Create a QFont object and set its properties
        font_id = QFontDatabase.addApplicationFontFromData(font_file.readAll())
        font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_name)
        ########################################################################
        for widget in app.allWidgets():
            widget.setFont(font)
        
        #########################################################################
        # This section contains the Binary Header for the software trading view #
        #########################################################################
        
        ########################################################################
        ########################################################################
    
    def update_header(self, updatePriceFunction, updatePriceFunction_2, updatePriceFunction_3, updatePriceFunction_4):
        self.updatePrice.display(updatePriceFunction)
        self.updatePrice_2.display(updatePriceFunction_2)
        self.updatePrice_3.display(updatePriceFunction_3)
        self.updatePrice_4.display(updatePriceFunction_4)

        if updatePriceFunction > 78:
            self.updateLabel.hide()
            self.updateLabel_6.show()

        elif updatePriceFunction <= 75:
            self.updateLabel.show()
            self.updateLabel_6.hide()

        if updatePriceFunction_2 > 85:
            self.updateLabel_2.hide()
            self.updateLabel_7.show()

        elif updatePriceFunction_2 <= 80:
            self.updateLabel_2.show()
            self.updateLabel_7.hide()

        if updatePriceFunction_3 > 85:
            self.updateLabel_3.hide()
            self.updateLabel_8.show()

        elif updatePriceFunction_3 <= 75:
            self.updateLabel_3.show()
            self.updateLabel_8.hide()

        if updatePriceFunction_4 > 76:
            self.updateLabel_4.hide()
            self.updateLabel_9.show()
            
        elif updatePriceFunction_4 <= 82:
            self.updateLabel_4.show()
            self.updateLabel_9.hide()

    def gotoinfopage(self):
        self.User_form.hide()
        self.trendpage.hide()
        self.bodyContent.show()
        self.stackedWidget.setCurrentWidget(self.infoPage)

    def gotohelppage(self):
        self.User_form.hide()
        self.trendpage.hide()
        self.bodyContent.show()
        self.stackedWidget.setCurrentWidget(self.helpPage)

    def on_pair_selected(self, selected_pair):
        self.telegram_thread = TelegramCrawlerThread(selected_pair)
        self.telegram_thread.signal.connect(self.update_data)
        self.telegram_thread.start()

    def homeContent(self):
        self.trendpage.hide()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.bodyContent.show()
        self.stackedWidget.setCurrentWidget(self.homePage)

    def subscriptionPageFunction(self):
        self.openAccBtn.hide()
        self.closeAccBtn.hide()
        self.trendpage.hide()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.bodyContent.show()
        self.stackedWidget.setCurrentWidget(self.subscriptionPage)

    def trendingsFunc(self):
        self.openAccBtn.hide()
        self.closeAccBtn.hide()
        self.trendpage.hide()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.bodyContent.show()
        self.stackedWidget.setCurrentWidget(self.telegramTrends)

    def delayresult(self):
        self.signalBanner.hide()
        self.getPairButton.hide()
        self.comboPair.hide()
        self.comboTimer.hide()
        self.connectingLabel.show()
        self.connectingLabel.setText("Getting signal")
        QtCore.QTimer.singleShot(4000, lambda: self.connectingLabel.setText("Getting signal please wait..."))
        QtCore.QTimer.singleShot(5000, lambda: self.connectingLabel.setText("Getting signal please wait"))
        QtCore.QTimer.singleShot(6000, lambda: self.connectingLabel.setText("Getting signal please wait."))
        QtCore.QTimer.singleShot(7000, lambda: self.connectingLabel.setText("Getting signal please wait.."))
        QtCore.QTimer.singleShot(8000, lambda: self.connectingLabel.setText("Getting signal please wait..."))
        QtCore.QTimer.singleShot(9500, lambda: self.connectingLabel.setText("Please place your trade and monitor the timer, do not let forget to check fxsignalspot."))
        QtCore.QTimer.singleShot(13500, lambda: self.connectingLabel.setText("Visit fxsignalspot at https://www.fxsignalspot.com."))
        QtCore.QTimer.singleShot(17500, lambda: self.connectingLabel.setText("Subscribe to our service to get the best Binary Forecast, <br> Check our Subscription page for more details."))
        QtCore.QTimer.singleShot(21500, lambda: self.connectingLabel.setText("Please hold on, you can't place another trade until this session as been exhausted."))
        QtCore.QTimer.singleShot(25500, lambda: self.connectingLabel.setText("From fxsignalspot we wish you a successful trading experience."))
        QtCore.QTimer.singleShot(29500, lambda: self.connectingLabel.setText("Please place your trade and monitor the timer, do not let forget to check fxsignalspot."))
        QtCore.QTimer.singleShot(33500, lambda: self.connectingLabel.setText("Visit fxsignalspot at https://www.fxsignalspot.com."))
        QtCore.QTimer.singleShot(37500, lambda: self.connectingLabel.setText("Subscribe to our service to get the best Binary Forecast, <br> Check our Subscription page for more details."))
        QtCore.QTimer.singleShot(41500, lambda: self.connectingLabel.setText("Please hold on, you can't place another trade until this session as been exhausted."))
        QtCore.QTimer.singleShot(45500, lambda: self.connectingLabel.setText("From fxsignalspot we wish you a successful trading experience."))
        QtCore.QTimer.singleShot(49500, lambda: self.connectingLabel.setText("Please place your trade and monitor the timer, do not let forget to check fxsignalspot."))
        QtCore.QTimer.singleShot(53500, lambda: self.connectingLabel.setText("Visit fxsignalspot at https://www.fxsignalspot.com."))
        QtCore.QTimer.singleShot(57500, lambda: self.connectingLabel.setText("Subscribe to our service to get the best Binary Forecast, <br> Check our Subscription page for more details."))
        QtCore.QTimer.singleShot(61500, lambda: self.connectingLabel.setText("Please hold on, you can't place another trade until this session as been exhausted."))
        QtCore.QTimer.singleShot(65500, lambda: self.connectingLabel.setText("From fxsignalspot we wish you a successful trading experience."))
        QtCore.QTimer.singleShot(69500, lambda: self.connectingLabel.setText("Subscribe to our service to get the best Binary Forecast, <br> Check our Subscription page for more details."))
        QtCore.QTimer.singleShot(73500, lambda: self.connectingLabel.setText("Please hold on, you can't place another trade until this session as been exhausted."))
        QtCore.QTimer.singleShot(77500, lambda: self.connectingLabel.setText("From fxsignalspot we wish you a successful trading experience."))
        QtCore.QTimer.singleShot(81500, lambda: self.connectingLabel.setText("Subscribe to our service to get the best Binary Forecast, <br> Check our Subscription page for more details."))
        QtCore.QTimer.singleShot(85500, lambda: self.connectingLabel.setText("Please hold on, you can't place another trade until this session as been exhausted."))
        QtCore.QTimer.singleShot(89500, lambda: self.connectingLabel.setText("From fxsignalspot we wish you a successful trading experience."))
     
    #Trade Pair to Setup
    def trendings(self):
        # code for displaying signal screen
        self.User_form.hide()
        self.trendpage.show()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.bodyContent.hide()
        self.telegramNotification.hide()

        fixedPair = ['EUR/USD', 'AUD/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD', 'NZD/USD', 'AUD/CAD', 'AUD/CHF', 'AUD/JPY', 'AUD/NZD', 'CAD/CHF', 'CAD/JPY', 'CHF/JPY', 'EUR/AUD', 'EUR/CAD', 'EUR/CHF', 'EUR/GBP', 'EUR/JPY', 'EUR/NZD', 'GBP/AUD', 'GBP/CAD', 'GBP/CHF', 'GBP/JPY', 'GBP/NZD', 'NZD/CAD', 'NZD/CHF', 'NZD/JPY', 'XAU/USD']
        self.combo_1 = self.findChild(QComboBox, "comboPair")
        self.trade_pair = fixedPair
        self.trade_pair_list = list(self.trade_pair)
        self.combo_1.addItems(self.trade_pair_list)
        self.combo_1.setCurrentText("EUR/USD")
        
        # Add a button to get the selected trading pair and rate
        self.get_pair_button = self.findChild(QPushButton, "getPairButton")
        self.get_pair_button.clicked.connect(self.runSignal)
    
    def init_web_view(self):
        conn = sqlite3.connect("components/fxglobal.db")
        cur = conn.cursor()
        cur.execute("SELECT youtube FROM Links ORDER BY id DESC LIMIT 1")
        result = cur.fetchone()

        if result:
            video_url = result[0]
            trendpage = self.advert
            if hasattr(self, 'web_view'):
                self.web_view.deleteLater()
                self.web_view = None
            self.web_view = QWebEngineView()
            self.web_view.setUrl(QUrl(video_url + str("?autoplay=1")))
            self.web_view.loadFinished.connect(self.enter_fullscreen)
            trendpage.layout().addWidget(self.web_view)

    def enter_fullscreen(self):
        self.web_view.page().runJavaScript("document.querySelector('iframe').requestFullscreen();")
    
    def showAds(self):
        self.init_web_view()
        self.binaryUpdateHeader.hide()
        self.advert.show()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.bodyContent.hide()
        self.telegramNotification.hide()
        self.timerBar_3.show()
        self.headerMenuContainer.hide()
        self.menuContainer.hide()
        self.showAdsBtn.hide()
        self.signalContainer.hide()
        self.telegramCurrency.show()

    def hideAds(self):
        self.init_web_view()
        self.binaryUpdateHeader.show()
        self.telegramCurrency.hide()
        self.timerBar_3.hide()
        self.advert.hide()
        self.binaryScreen.show()
        self.hideAdsBtn.hide()
        self.showAdsBtn.hide()
        self.signalContainer.show()
        self.menuContainer.hide()
        self.headerMenuContainer.show()
        
    def get_trading_pairs_from_combo_box(self):
        try:
            self.selected_pair = self.combo_1.currentText()
            selected_pair = self.combo_1.currentText()
            if selected_pair not in self.trade_pair:
                QMessageBox.about(self, "Notice", "<strong><small><center>You either did not select any Trading Pair or your Trading Pair is not found in the list.</center></small></strong>")
            else:
                base_currency = selected_pair.split("/")[0]
                quote_currency = selected_pair.split("/")[1]

                base_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

                # Make a GET request to the API
                response = requests.get(base_url)

                # Check the status code of the response to make sure it was successful
                if response.status_code == 200:
                    # Parse the response data as JSON
                    data = response.json()

                    # Get the exchange rate for the selected pair from the response data
                    rate = data['rates'][quote_currency]

                    # Return the currency pair and exchange rate as a tuple
                    return (selected_pair, rate)
                else:
                    # If the request was not successful, return None
                    return None
        except Exception as e:
            QMessageBox.about(self, "Notice", "<strong><small><center>An Error Occurred</center></small></strong><br> <p><small></small></p><br/>" + str(e))

    def display_message(self):
        self.signalLabel.show()
        self.telegramAction.hide()
        self.telegramAction_2.hide()
        QtCore.QTimer.singleShot(1000, lambda: self.signalLabel.setText(str("Wait.")))
        QtCore.QTimer.singleShot(2000, lambda: self.signalLabel.setText(str("Wait..")))
        QtCore.QTimer.singleShot(3000, lambda: self.signalLabel.setText(str("Wait...")))
        QtCore.QTimer.singleShot(4000, lambda: self.signalLabel.setText(str("Wait.")))
        QtCore.QTimer.singleShot(5000, lambda: self.signalLabel.setText(str("Wait..")))
        QtCore.QTimer.singleShot(6000, lambda: self.signalLabel.setText(str("Wait...")))
        QtCore.QTimer.singleShot(7000, lambda: self.signalLabel.setText(str("Wait.")))
        QtCore.QTimer.singleShot(8000, lambda: self.signalLabel.setText(str("Wait..")))
        QtCore.QTimer.singleShot(9000, lambda: self.signalLabel.hide())


    def get_selected_pair(self):
        try:
            # Get the selected trading pair and rate
            selected_pair, rate = self.get_trading_pairs_from_combo_box()
            if selected_pair is None:
                QMessageBox.about(self, "Notice", "<strong><small><center>You either did not select any Trading Pair or your Trading Pair is not found in the list.</center></small></strong>")
            else:
                #set to a label
                self.labelPair.setText(selected_pair)
                self.labelPair_1.setText(str(rate))

                # Calculate the signal strength (you can use any method you want to calculate the signal strength)
                signal_strength = rate * 80
                
                # Update the progress bar to show the signal strength
                self.progress_bar = self.findChild(QProgressBar, "strengthBar")
                self.progress_bar.setValue(round(int(signal_strength)))
                getstrengthBar = self.progress_bar.setValue(int(signal_strength))

                signal_strength = random.uniform(0.85, 0.95)
                getPercentage = round(int(signal_strength*100), 3)
                self.strengthBar_5.setText(str(getPercentage) + " %")
        except Exception as e:
            QMessageBox.about(self, "Notice", "<center><strong><small><center>An Error Occurred</center></small></strong><br> <p><small>Check your Network Connection!!!</small></p></center><br/>" + str(e))

    def start_timer_thread(self,counter_value):
        self.my_thread.counter = counter_value
        self.my_thread.start()
    
    def combo_selection_changed(self):
        combo_value = self.combo_2.currentText()
        if combo_value == "1 mins":
            counter_value = 60
        elif combo_value == "2 mins":
            counter_value = 120
        elif combo_value == "3 mins":
            counter_value = 180
        elif combo_value == "4 mins":
            counter_value = 240
        elif combo_value == "5 mins":
            counter_value = 300
        elif combo_value == "10 mins":
            counter_value = 600
        elif combo_value == "15 mins":
            counter_value = 900
        elif combo_value == "30 mins":
            counter_value = 1800
        elif combo_value == "1 hrs":
            counter_value = 3600
        elif combo_value == "2 hrs":
            counter_value = 7200
        elif combo_value == "3 hrs":
            counter_value = 10800
        elif combo_value == "4 hrs":
            counter_value = 14400
        elif combo_value == "5 hrs":
            counter_value = 18000

        self.start_timer_thread(counter_value)

    def adminLoginFunction(self):
        user = self.adminUser.text()
        password = self.adminPassword.text()

        if len(user) == 0 or len(password) == 0:
            self.adminMessage.setText("Please fill all Fields !!! ")
            return

        try:
            adminName = "fxsignalspot"
            adminPass = "@Avalanche_1998_1991_06"

            if user == adminName and password == adminPass:
                QtCore.QTimer.singleShot(1000, lambda: self.youtubeName.show())
                QtCore.QTimer.singleShot(1000, lambda: self.saveYoutube.show())
                QtCore.QTimer.singleShot(1000, lambda: self.adminYoutube.show())
                QtCore.QTimer.singleShot(1000, lambda: self.adminUser.hide())
                QtCore.QTimer.singleShot(1000, lambda: self.adminPassword.hide())
                QtCore.QTimer.singleShot(1000, lambda: self.adminLogin.hide())
                self.adminMessage.setText("Login Successful !!! ")
            else:
                self.adminMessage.setText("Password or Username incorrect !!! ")

        except Exception as e:
            QMessageBox.about(self, "Notice", "<strong><small><center>An Error Occurred</center></small></strong><br> <p><small></small></p><br/>" + str(e))

    def saveYoutubeFunction(self):
        try:            
            youtube = self.adminYoutube.text()
            youtubeLabel = self.youtubeName.text()

            if len(youtube) == 0 or len(youtubeLabel) == 0:
                self.adminMessage.setText("Please fill all Fields !!! ")

            else:
                conn = sqlite3.connect("components/fxglobal.db")
                cur = conn.cursor()

                Links = (youtube, youtubeLabel)
                cur.execute("INSERT INTO Links (youtube, youtubeLabel) VALUES(?,?)", Links)

                conn.commit()
                self.adminMessage.setText("<strong><small><center>You have Successfully added the Youtube Link</center></small></strong>")
                QtCore.QTimer.singleShot(1000, lambda: self.youtubeName.hide())
                QtCore.QTimer.singleShot(1000, lambda: self.saveYoutube.hide())
                QtCore.QTimer.singleShot(1000, lambda: self.adminYoutube.hide())
                QtCore.QTimer.singleShot(1000, lambda: self.adminUser.show())
                QtCore.QTimer.singleShot(1000, lambda: self.adminPassword.show())
                QtCore.QTimer.singleShot(1000, lambda: self.adminLogin.show())

        except Exception as e:
            QMessageBox.about(self, "Notice", "<strong><small><center>An Error Occurred</center></small></strong><br> <p><small>Please be sure you are connected to the Internet to use this Service.</small></p><br/><small><p>Check that your Username, First Name and Last Name are different from previous Logged in Details</p></small><br/>" + str(e))

    def update_progress_bar(self, display_text):
        hours, minutes, seconds = map(int, display_text.split(':'))
        total_seconds = 3600*hours + 60*minutes + seconds
        self.timerBar_3.display(display_text)
        if total_seconds <= 30:
            self.signalLabel.hide()
            self.timerBar.hide()
            self.timerBar_2.show()
            self.telegramAction.hide()
            self.telegramAction_2.show()
            QtCore.QTimer.singleShot(1000, lambda: self.telegramAction_2)
            QtCore.QTimer.singleShot(1500, lambda: self.telegramAction_2.hide())
            QtCore.QTimer.singleShot(1500, lambda: self.telegramAction.show())
            QtCore.QTimer.singleShot(2000, lambda: self.telegramAction)
            QtCore.QTimer.singleShot(2000, lambda: self.telegramAction_2.show())
            QtCore.QTimer.singleShot(2000, lambda: self.telegramAction.hide())
            QtCore.QTimer.singleShot(2500, lambda: self.telegramAction_2)
            QtCore.QTimer.singleShot(2500, lambda: self.telegramAction_2.hide())
            QtCore.QTimer.singleShot(2500, lambda: self.telegramAction.show())
            QtCore.QTimer.singleShot(3000, lambda: self.telegramAction)
            QtCore.QTimer.singleShot(3500, lambda: self.telegramAction_2.hide())
            QtCore.QTimer.singleShot(3000, lambda: self.telegramAction.hide())
            self.timerBar_2.display(display_text)
        
        elif total_seconds == 60:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(50000, lambda: self.hideAds())
        
        elif total_seconds == 120:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(100000, lambda: self.hideAds())
        
        elif total_seconds == 180:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(150000, lambda: self.hideAds())

        elif total_seconds == 240:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(200000, lambda: self.hideAds())

        elif total_seconds == 300:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(250000, lambda: self.hideAds())

        elif total_seconds == 600:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(300000, lambda: self.hideAds())

        elif total_seconds == 900:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(350000, lambda: self.hideAds())

        elif total_seconds == 1800:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(400000, lambda: self.hideAds())

        elif total_seconds == 3600:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(450000, lambda: self.hideAds())

        elif total_seconds == 7200:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(500000, lambda: self.hideAds())

        elif total_seconds == 10800:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(550000, lambda: self.hideAds())

        elif total_seconds == 14400:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(600000, lambda: self.hideAds())

        elif total_seconds == 18000:
            QtCore.QTimer.singleShot(18000, lambda: self.showAds())
            QtCore.QTimer.singleShot(650000, lambda: self.hideAds())
        
        else:
            self.timerBar.show()
            self.timerBar_2.hide()
            self.telegramAction.show()
            self.telegramAction_2.hide()
            self.timerBar.display(display_text)

    def reset(self):
        QtCore.QTimer.singleShot(3500, lambda: self.signalLabel.show())
        QtCore.QTimer.singleShot(3500, lambda: self.signalLabel.setText(" "))
        QtCore.QTimer.singleShot(3500, lambda: self.telegramAction.hide())
        self.label.show()
        self.headerMenuContainer.show()
        self.labelPair_1.show()
        self.menuContainer.show()
        self.frame_4.show()
        self.networkStrength.show()
        self.getPairButton.show()
        self.comboPair.show()
        self.comboTimer.show()
        self.signalBanner.hide()
        self.signalBanner_2.hide()
        self.connectingLabel.hide()
        self.strengthBar_5.setText(" ")
        self.combo_1 = self.findChild(QComboBox, "comboPair")
        self.combo_1.setCurrentText("EUR/USD")
        self.combo_2 = self.findChild(QComboBox, "comboTimer")
        self.combo_2.setCurrentText("1 mins")

    def update_data(self, signal, currency, entry, time):
        self.telegramAction.setText(f'Signal: {signal}')
        self.telegramAction_2.setText(f'Currency: {currency}')
        self.telegramAction_3.setText(f'Entry: {entry}')
        self.telegramEntry.setText(entry)
        self.telegramCurrency.setText(currency)
        self.telegramTime.setText(time)

    def runSignal(self):
        self.get_selected_pair()
        self.combo_selection_changed()
        self.delayresult()
        self.display_message()
        self.label.hide()
        self.headerMenuContainer.hide()
        self.frame_4.hide()
        self.labelPair_1.hide()
        self.menuContainer.hide()
        self.strengthBar.show()
        selected_pair = self.combo_1.currentText()
        plain_pair = selected_pair
        plain_trade_pair = plain_pair.replace('/', '')
        tc = TelegramCrawler()
        tc.init(plain_trade_pair)
        signal, currency, entry, time = tc.get_result()
        self.telegramAction_2.setText(signal)
        self.labelPair.hide()
        self.labelPair_1.hide()
        QtCore.QTimer.singleShot(1000, lambda: self.telegramAction.hide())
        QtCore.QTimer.singleShot(9000, lambda: self.telegramAction.setText(signal))
        QtCore.QTimer.singleShot(9000, lambda: self.telegramAction.show())
        QtCore.QTimer.singleShot(10000, lambda: self.strengthBar_5.show())
        QtCore.QTimer.singleShot(10000, lambda: self.labelPair.show())
        self.telegramEntry.setText(entry)
        self.telegramEntry.hide()
        self.telegramCurrency.setText(currency)
        self.telegramCurrency.hide()
        self.telegramTime.setText(time)
        self.telegramTime.hide()
        if signal == 'Buy\nCurrency':
            QtCore.QTimer.singleShot(9000, lambda: self.signalBanner.show())
            QtCore.QTimer.singleShot(9000, lambda: self.signalBanner_2.hide())
        elif signal == 'Sell\nCurrency':
            QtCore.QTimer.singleShot(9000, lambda: self.signalBanner.hide())
            QtCore.QTimer.singleShot(9000, lambda: self.signalBanner_2.show())
        else:
            QtCore.QTimer.singleShot(9000, lambda: self.signalBanner.hide())
            QtCore.QTimer.singleShot(9000, lambda: self.signalBanner_2.hide())

    def light(self):
        self.darkMode.show()
        self.lightMode.hide()

    def black(self):
        self.darkMode.hide()
        self.lightMode.show()

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 or len(password) == 0:
            self.message.setText("Please fill all Fields !!! ")
            return

        try:
            conn = sqlite3.connect("components/fxglobal.db")
            cur = conn.cursor()
            query = 'SELECT password FROM users WHERE username =\''+user+'\''
            cur.execute(query)
            result_pass = cur.fetchone()
            if result_pass:
                result_pass = result_pass[0]
                # hash the input password using sha256
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if hashed_password == result_pass:
                    self.message.setText("Login Successful !!! ")
                    QtCore.QTimer.singleShot(2000, lambda: self.homePageFunction())
                    if self.remember_me_checkbox.isChecked():
                        data = {"username": user, "password": password}
                        with open("login_details.json", "w") as f:
                            json.dump(data, f)
                    else:
                        try:
                            os.remove("login_details.json")
                        except:
                            pass
                else:
                    self.message.setText("Password or Username incorrect !!! ")
            else:
                self.message.setText("Password or Username incorrect !!! ")
        except Exception as e:
                QMessageBox.about(self, "Notice", "<strong><small><center>An Error Occurred</center></small></strong><br> <p><small></small></p><br/>" + str(e))

    def check_saved_login(self):
        try:
            with open("login_details.json", "r") as f:
                data = json.load(f)
                self.emailfield.setText(data["username"])
                self.passwordfield.setText(data["password"])
                self.remember_me_checkbox.setChecked(True)
        except:
            pass

    def signupfunction(self):
        try:
            name = self.namerfield.text()
            username = self.usernamerfield.text()
            email = self.emailfield_2.text()
            password = self.passwordfield_2.text()
            confirmpassword = self.confirmpassword.text()

            # Check if all fields are filled
            if len(username) == 0 or len(password) == 0 or len(confirmpassword) == 0 or len(name) == 0 or len(email) == 0:
                self.message_2.setText("Please fill all Fields !!! ")

            # Check if passwords match
            elif password!=confirmpassword:
                self.message_2.setText("Password do not match !!! ")

            # Check if email is valid
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                self.message_2.setText("Invalid email address !!! ")

            else:
                conn = sqlite3.connect("components/fxglobal.db")
                cur = conn.cursor()
                password = hashlib.sha256(password.encode()).hexdigest()
                Users = (username, password, name, email)
                cur.execute('INSERT INTO users (username, password, name, email) VALUES(?,?,?,?)', Users)
                conn.commit()
                self.message_2.setText("<strong><small><center>User Successfully Signed Up, click again to proceed.</center></small></strong>")
                QtCore.QTimer.singleShot(2000, lambda: self.homePageFunction())
        except Exception as e:
            QMessageBox.about(self, "Notice", "<strong><small><center>An Error Occurred</center></small></strong><br> <p><small>Please be sure you are connected to the Internet to use this Service.</small></p><br/><small><p>Check that your Username, Email are different from previous Logged in Details</p></small><br/>")

    def logoutFunction(self):
        self.headerMenuContainer.hide()
        self.menuContainer.hide()
        self.User_form.hide()
        self.loginForm.show()
        self.signUpForm.hide()
        self.bodyContent.hide()
        self.trendpage.hide()
        self.telegramNotification.hide()
        self.hideNotificationBtn.hide()
        self.hideBtn.hide()
        self.fullMenu.hide()
        self.message.setText("You logged out.")

    def login_Form(self):
        self.User_form.hide()
        self.loginForm.show()
        self.signUpForm.hide()
        self.bodyContent.hide()
        self.trendpage.hide()
        self.telegramNotification.hide()

    def sign_Up_Form(self):
        self.User_form.hide()
        self.signUpForm.show()
        self.loginForm.hide()
        self.trendpage.hide()
        self.bodyContent.hide()
        self.telegramNotification.hide()

    def User_form_function(self):
        self.User_form.show()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.bodyContent.hide()
        self.trendpage.hide()
        self.telegramNotification.hide()

    def expand(self):
        self.bodyContent.hide()
        self.expandBtn.hide()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.restoreBtn.show()

    def openAcc(self):
        self.signUpBtn.show()
        self.logInBtn.show()
        self.openAccBtn.hide()
        self.closeAccBtn.show()
        self.expandBtn.hide()
        self.restoreBtn.hide()
        self.stackedWidget_2.hide()
        self.telegramNotification.show()

    def closeAcc(self):
        self.bodyContent.show()
        self.trendpage.hide()
        self.signUpForm.hide()
        self.loginForm.hide()
        self.signUpBtn.hide()
        self.logInBtn.hide()
        self.openAccBtn.show()
        self.closeAccBtn.hide()
        self.telegramNotification.hide()
    
    def homePageFunction(self):
        self.iconMenu.show()
        self.notificationBtn.show()
        self.menuContainer.show()
        self.rightMenu.show()
        self.headerMenuContainer.show()
        self.menuSubContainer.show()
        self.sizeSetting.show()
        self.showBtn.show()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.trendpage.hide()
        self.telegramNotification.hide()
        self.bodyContent.show()
        self.stackedWidget.setCurrentWidget(self.homePage)

    def restore(self):
        self.bodyContent.show()
        self.expandBtn.show()
        self.restoreBtn.hide()
        self.loginForm.hide()
        self.signUpForm.hide()

    def showTelegramChannel(self):
        self.telegramNotification.show()
        self.hideNotificationBtn.hide()
        self.notificationBtn.show()
        self.closeChannelBtn.show()
        self.closeChannelBtn_2.show()
        self.telegramBtn.hide()
        self.telegramBtn_2.hide()
        self.stackedWidget_2.setCurrentWidget(self.telegramPage)
        
    def showNotification(self):
        self.expandBtn.show()
        self.restoreBtn.hide()
        self.telegramNotification.show()
        self.notificationBtn.hide()
        self.hideNotificationBtn.show()
        self.closeChannelBtn.hide()
        self.closeChannelBtn_2.hide()
        self.telegramBtn.show()
        self.telegramBtn_2.show()
        self.stackedWidget_2.setCurrentWidget(self.notificationPage)

    def closeChannel(self):
        self.telegramNotification.hide()
        self.notificationBtn.show()
        self.hideNotificationBtn.hide()
        self.closeChannelBtn.hide()
        self.closeChannelBtn_2.hide()
        self.telegramBtn.show()
        self.telegramBtn_2.show()
        self.stackedWidget_2.setCurrentWidget(self.telegramPage)

    def hideNotification(self):
        self.expandBtn.show()
        self.restoreBtn.hide()
        self.loginForm.hide()
        self.signUpForm.hide()
        self.telegramNotification.hide()
        self.notificationBtn.show()
        self.hideNotificationBtn.hide()
        self.closeChannelBtn.hide()
        self.closeChannelBtn_2.hide()
        self.telegramBtn.show()
        self.telegramBtn_2.show()
        self.stackedWidget_2.setCurrentWidget(self.notificationPage)

    def showMenu(self):
        self.fullMenu.show()
        self.iconMenu.hide()
        self.showBtn.hide()
        self.hideBtn.show()

    def hideMenu(self):
        self.fullMenu.hide()
        self.iconMenu.show()
        self.showBtn.show()
        self.hideBtn.hide()

    def progress(self):
        global counter

        self.progressBar.setValue(counter)

        if counter > 100:
            self.timer.stop()
            self.User_form.hide()
            self.headerMenuContainer.hide()
            self.proceedBtn.hide()
            self.menuSubContainer.hide()
            self.fullMenu.hide()
            self.sizeSetting.hide()
            self.hideBtn.hide()
            self.showBtn.hide()
            self.bodyContent.hide()
            self.progressBarContainer.hide()
            self.telegramNotification.hide()
            self.hideNotificationBtn.hide()
            self.closeChannelBtn.hide()
            self.restoreBtn.hide()
            self.closeAccBtn.hide()
            self.signUpBtn.hide()
            self.logInBtn.hide()
            self.loginForm.show()
            self.signUpForm.hide()
            self.darkMode.hide()
            self.trendpage.hide()
            self.closeChannelBtn_2.hide()
            self.advert.hide()
            self.hideAdsBtn.hide()
            self.showAdsBtn.hide()
            self.timerBar.hide()
            self.timerBar_2.show()
            self.connectingLabel.hide()
            self.signalBanner.hide()
            self.signalBanner_2.hide()
            self.telegramAction.hide()
            self.telegramAction_2.hide()
            self.strengthBar_5.hide()
            self.strengthBar.hide()
            self.openAccBtn.hide()
            self.timerBar_3.hide()
            self.label.hide()
            self.networkStrength.hide()
            self.labelPair_1.hide()
            self.set_font_on_widgets()
        else:
            self.strengthBar.hide()
            self.networkStrength.hide()
            self.openAccBtn.hide()
            self.closeAccBtn.hide()
            self.lightMode.hide()
            self.darkMode.hide()
            self.User_form.hide()
            self.strengthBar_5.hide()
            self.telegramAction.hide()
            self.telegramAction_2.hide()
            self.signalBanner.hide()
            self.signalBanner_2.hide()
            self.connectingLabel.hide()
            self.restoreBtn.hide()
            self.headerMenuContainer.hide()
            self.proceedBtn.hide()
            self.menuSubContainer.hide()
            self.sizeSetting.hide()
            self.telegramNotification.hide()
            self.hideNotificationBtn.hide()
            self.closeChannelBtn.hide()
            self.closeAccBtn.hide()
            self.signUpBtn.hide()
            self.logInBtn.hide()
            self.loginForm.hide()
            self.signUpForm.hide()
            self.darkMode.hide()
            self.trendpage.hide()
            self.closeChannelBtn_2.hide()
            self.advert.hide()
            self.hideAdsBtn.hide()
            self.showAdsBtn.hide()
            self.timerBar.hide()
            self.timerBar_2.show()
        counter +=1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome=ApplicationScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    app.setApplicationName("FXsignalspot")
    app.setWindowIcon(QIcon("components/icons/fxsignalspot.png"))
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")