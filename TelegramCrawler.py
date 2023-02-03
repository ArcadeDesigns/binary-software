import os
import sys
import asyncio
from telethon import TelegramClient
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler

class TelegramCrawler:
    def __init__(self):
        self.telegram_message = None
        self.telegram_signal = None
        self.telegram_entry = None
        self.telegram_currency = None
        self.telegram_entry_time = None

    def init(self, selected_pair):
        # Create a Telegram client
        self.client = TelegramClient('session_name', api_id='#########', api_hash='################################')

        # Connect to Telegram servers
        try:
            self.client.start()
        except Exception as e:
            print("Error: " + str(e))
            return

        # Get the messages from the channel
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_messages(selected_pair))
        self.client.disconnect()

    async def get_messages(self, selected_pair):
        message_found = False
        messages = await self.client.get_messages('https://t.me/##################', limit=10)
        try:
            self.telegram_data = []
            for message in messages:
                plain_pair = selected_pair
                plain_trade_pair = plain_pair.replace('/', '')
                if "Currency: " + plain_trade_pair in message.message:
                    self.telegram_message = message.message
                    message_parts = message.message.split(',')
                    for part in message_parts:
                        if "Signal:" in part:
                            # added strip() to remove any whitespaces before or after the signal
                            self.telegram_signal = part.split(":")[1].strip()
                        if "Currency:" in part:
                            self.telegram_currency = part.split(":")[2].strip()
                        if "Entry Price:" in part:
                            # added strip() to remove any whitespaces before or after the entry
                            self.telegram_entry = part.split(":")[3].strip()
                        if "Entry Time:" in part:
                            # added strip() to remove any whitespaces before or after the entry
                            self.telegram_entry_time = part.split(":")[4].strip()
                            self.telegram_data.append({"signal": self.telegram_signal, "currency": self.telegram_currency, "entry": self.telegram_entry, "time": self.telegram_entry_time})
                            message_found = True
                            break
            if not message_found:
                self.telegram_message = "No messages found containing the selected pair."
                self.telegram_signal = "Subscribe <br> to our <br> Premuim <br> Version"
                self.telegram_entry = "Not Available"
                self.telegram_currency = "Not Available"
                self.telegram_entry_time = "Not Available"

        except Exception as e:
            print("Error: " + str(e))
        
    def get_result(self):
        return self.telegram_signal, self.telegram_currency, self.telegram_entry, self.telegram_entry_time
    
if __name__ == '__main__':
    tc = TelegramCrawler()
    print(tc.get_result())
