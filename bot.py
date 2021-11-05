import json
import colorama 
import os
import time

from PIL import Image
from colorama import Fore
from util.error import NoDigit
from util.commands import Commands
from typing import Union
from util.twitter import Twitter

colorama.init(autoreset=True)

class main:
    def __init__(self):

        try:
            print(Fore.GREEN + "Loading settings..")
            config = json.loads(open("config.json").read()) # load configurations

            self.language = config.get('language')
            self.searchlanguage = config.get('searchLanguage')         
            self.mergeauto = config.get('mergeauto')
            twitter = config.get('twitter', {})
            self.twitter = None
            self.newcosmeticsText = twitter.get('newcosmeticsText', '')
            self.pakText = twitter.get('pakText', '')
            if twitter.get('enabled'):
                apiKey = twitter.get('apiKey')
                apiSecret = twitter.get('apiSecret')
                accessToken = twitter.get('accessToken')
                accessTokenSecret = twitter.get('accessTokenSecret')
                self.twitter = Twitter(
                    apiKey, apiSecret, accessToken, accessTokenSecret
                )
            else:
                self.twitter = False
            
        except Exception as e:
            print(Fore.RED + f"{e}")
        except FileNotFoundError as e:
            print(Fore.RED + f"{e}")
        time.sleep(3)
        os.system('cls')


    # ==> Main Thread
    def main(self):
        #SystemUtil(self).change_title()
        self.w()
        choice = input('>> ')
        try:
            check_choice = self.inputs(choice)
        except NoDigit:
            print('No Digit')
            return 0

        if check_choice:
            check_choice()
        else:
            print("Command not available")


    def w(self) -> None:
        print(Fore.GREEN + f"Welcome {os.environ['username']} in this program!\nThis program is be able to generate new cosmetics, search for items and sets.\nBelow you have a list of features, choose!")
        print("")
        print(Fore.GREEN + "\n- - - - - MENU - - - - -")
        print("")
        print(Fore.YELLOW + "(1)" + Fore.GREEN + " - Generate newcosmetics")
        print(Fore.YELLOW + "(2)" + Fore.GREEN + " - Search for a cosmetics")
        print(Fore.YELLOW + "(3)" + Fore.GREEN + " - Search for a pak")
        print(Fore.YELLOW + "(4)" + Fore.GREEN + " - Merge images in cache folder")
        print(Fore.YELLOW + "(5)" + Fore.GREEN + " - New Features")



    def inputs(self, x: Union[str, int, None]):
        newcosm = Commands(self)
        searchcosm = Commands(self)
        pak = Commands(self)
        merge = Commands(self)
        features = Commands(self)

        choices = {
            1: newcosm.NewCosmetics,
            2: searchcosm.SearchCosmetic,
            3: pak.paksearch,
            4: merge.merge,
            5: features.feature
        }

        if isinstance(x, str):
            if x.isdigit():
                x = int(x)
            else:
                raise NoDigit

        return choices.get(x, None)       


if __name__ == '__main__':

    try:
        main().main()
    except KeyboardInterrupt:
        exit()
