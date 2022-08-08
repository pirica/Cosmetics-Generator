import tkinter as tk
import tkinter.messagebox
import json 
import os
import time 
import colorama
import requests

from colorama import Fore
from typing import Union
from datetime import datetime
from pypresence import Presence

from utils.TwitterManager import TwitterClient
from utils.CommandsManager import Commands
from utils.Errors import NoDigit


window = tk.Tk()
window.wm_withdraw()
colorama.init(autoreset=True)
client_id = "968816560309436457"

class Program:
    def __init__(self):
        self.start_time = datetime.now().timestamp()
        print(Fore.CYAN + "Cosmetics Generator made by ᴅᴊʟᴏʀ3xᴢᴏ\n" + Fore.GREEN + "Loading settings, please wait..")
        try:
            config = json.loads(open("configs.json").read())
            if not os.path.isdir('images'):
                os.makedirs('images')
            if not os.path.isdir('cache'):
                os.makedirs('cache')          
            self.language = config.get('language')
            self.searchLanguage = config.get('searchLanguage')
            self.newcosmeticsText = config.get('newCosmeticsText')
            self.newpakText = config.get('newPakText')
            if config.get('DiscordPresence'): 
                self.discord = True
                self.rpc = Presence(
                    client_id=client_id
                )
                self.rpc.connect()
                self.rpc.update(
                    details=f"Playing v{requests.get('https://fortnitecentral.gmatrixgames.ga/api/v1/aes').json()['version']}",
                    state="In menu",
                    large_image="app_image",
                    large_text="Cosmetic Generator",
                    small_text="User access",
                    start=int(self.start_time),
                    small_image="user_access",
                    buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
                )
            else: self.discord = False
            twitter = config.get('twitter', {})
            self.twitter = None
            if twitter.get('enabled'):
                apiKey = twitter.get('apiKey')
                apiSecret = twitter.get('apiSecret')
                accessToken = twitter.get('accessToken')
                accessTokenSecret = twitter.get('accessTokenSecret')
                self.twitter = TwitterClient(
                    apiKey, apiSecret, accessToken, accessTokenSecret
                )

            else:
                self.twitter = False

        except Exception as e:
            error = tkinter.messagebox.showerror(title="Error",message=f"An error accured:\n{e}", parent=window)
            if error == True:
                exit()
            else:
                exit()
        except FileNotFoundError as e:
            error = tkinter.messagebox.showerror(title="Error",message=f"An error accured:\n{e}", parent=window)
            if error == True:
                exit()
            else:
                exit()
        time.sleep(3)
        os.system('cls')

    def get_command_number(self):
        self.welcome_message()
        command = input('>> ')
        try:
            check_choice = self.inputs(command)
        except NoDigit:
            print(Fore.RED + "This option doesn't excist.")
            return 0

        if check_choice:
            check_choice()
        else:
            print("Command not available")

    def welcome_message(self) -> None:
        print(Fore.GREEN + f"Welcome {os.environ['username']} in Cosmetics Generator!\n"
                            "This program was created for people who need to generate cosmetics quickly and safely.\n"
                            "Below you have a list of features, choose!")
        print(Fore.CYAN + "Program made by ᴅᴊʟᴏʀ3xᴢᴏ - Copyright 2022-2023")
        print("")
        print(Fore.GREEN + "- OPTIONS MENU -")
        print("")
        print(Fore.YELLOW + "1) -" + Fore.GREEN + " Generate all newcosmetics of the latest patch")
        print(Fore.YELLOW + "2) -" + Fore.GREEN + " Search a cosmetics in-game")
        print(Fore.YELLOW + "3) -" + Fore.GREEN + " Search a pak and generate all cosmetics in it")
        print(Fore.YELLOW + "4) -" + Fore.GREEN + " Search for a set by name")
        print(Fore.YELLOW + "5) -" + Fore.GREEN + " Generate current news (br)")
        print(Fore.YELLOW + "6) -" + Fore.GREEN + " Merge images")

    def inputs(self, x: Union[str, int, None]):
        newcosm = Commands(self)
        searchcosm = Commands(self)
        pak = Commands(self)
        merge = Commands(self)
        news = Commands(self)

        choices = {
            1: newcosm.NewCosmetics,
            2: searchcosm.SearchCosmetic,
            3: pak.paksearch,
            4: searchcosm.set,
            5: news.NewsGenerator,
            6: merge.merge
        }

        if isinstance(x, str):
            if x.isdigit():
                x = int(x)
            else:
                raise NoDigit

        return choices.get(x, None)

if __name__ == "__main__":
    try:
        Program().get_command_number()
    except KeyboardInterrupt as e:
        print(e)
