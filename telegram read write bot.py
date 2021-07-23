# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 22:35:55 2021

@author: ACER - Ddhruv Arora
"""

import requests                
import json                     
import time

telegram_chat_id = "@xyz__"                                          # Telegram channel ID. Paste after @
telegram_bot_id  = "56-char-long-ID"  # telegram bot Id
base_url         = "https://api.telegram.org/" + telegram_bot_id        # final url

def send_telegram_message(message):  
    """Sends message via Telegram"""
    
    url = base_url + "/sendMessage"
    print("Sending message")
    
    data = { 
             "chat_id" : telegram_chat_id,
             "text"    : message 
           }
    
    try:
        response = requests.request("POST", url, params=data)
        #print( f"Telegram response: {response.text}" )
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    
    except Exception as e:
        print( f"An error occurred: {e}" )
        
    
def get_last_message():
    """ Gets last message from Telegram """
    
    url = base_url + "/getUpdates"
    print("Getting last message .....")
    
    try:
        response = requests.get(url)
        content = response.content.decode("utf8")
        js = json.loads(content)
        #print(js)
        num_updates = len(js["result"])
        last_update = num_updates - 1
        message_id = js["result"][last_update]["channel_post"]["message_id"]
        text = js["result"][last_update]["channel_post"]["text"]
        print("This is the last message : " + text)
        return (text, message_id)
    
    except Exception as e:
        print(f"An error occurred in getting message: {e}")
        

class log:

    def logging(self, last_text, last_message_id):
        """ logging data """
        fp = open("log.txt", "a")
        fp.write( str(last_text) + " - " + str(last_message_id) + "\n")
        
    def reading(self):
        """ reading logs """
        fp = open("log.txt", "r")
        last = fp.readlines()
        return ((last)[-1].split(" - "))


while True:
    
    x = log()
    last_text = x.reading()[1]
    last_message_id = x.reading()[0]
    #print(last_text, last_message_id)

    time.sleep(5)
    text, message_id = get_last_message()
    #print(text, message_id)
    
    if (text not in last_text or str(message_id) != last_message_id):
    
        if text == "hii":
            send_telegram_message("Hello")
            time.sleep(1)
        
    last_text = text
    last_message_id = message_id
    x.logging(last_message_id, last_text)
    