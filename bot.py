try:
    import tkinter as tk
    import tkinter.messagebox
    import json
    import colorama
    import os
    import time    

    from colorama import Fore
    from typing import Union

    from util.error import NoDigit
    from util.commands import Commands
    from util.twitter import Twitter
except ModuleNotFoundError as e:
    print(f"Error: {e}")

window = tk.Tk()
window.wm_withdraw()

colorama.init(autoreset=True)

class main:
    def __init__(self):
        colorama.init(autoreset=True)
        try:
            print(Fore.CYAN + "Cosmetics Generator made by ᴅᴊʟᴏʀ3xᴢᴏ\n" + Fore.GREEN + "Loading settings, please wait..")
            config = json.loads(open("config.json").read()) # load configurations
            self.language = config.get('language')
            self.searchlanguage = config.get('searchLanguage')  
            self.ChristmasIcon = config.get('christmasIcon')   
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
            error = tkinter.messagebox.showerror(title="Error",message=f"An error accured:\n{e}",parent=window)
            if error == True:
                exit()
            else:
                exit()
        except FileNotFoundError as e:
            error = tkinter.messagebox.showerror(title="Error",message=f"An error accured:\n{e}",parent=window)
            if error == True:
                exit()
            else:
                exit()
        time.sleep(3)
        os.system('cls')

    # ==> Main Thread
    def main(self):
        #SystemUtil(self).change_title()
        self.w()
        choice = input('')
        try:
            check_choice = self.inputs(choice)
        except NoDigit:
            print(Fore.RED + "This option doesn't excist.")
            return 0

        if check_choice:
            check_choice()
        else:
            print("Command not available")


    def w(self) -> None:
        print(Fore.GREEN + f"Welcome {os.environ['username']} in the Cosmetics Generator!\n"
                            "This program was created for people who need to generate cosmetics quickly and safely.\n"
                            "Below you have a list of features, choose!")
        print(Fore.CYAN + "Program made by ᴅᴊʟᴏʀ3xᴢᴏ - Copyright 2021")
        print("")
        print(Fore.GREEN + "- OPTIONS MENU -")
        print("")
        print(Fore.YELLOW + "1) -" + Fore.GREEN + " Generate all newcosmetics of the latest patch")
        print(Fore.YELLOW + "2) -" + Fore.GREEN + " Search a cosmetics in-game")
        print(Fore.YELLOW + "3) -" + Fore.GREEN + " Search a pak and generate all cosmetics in it")
        print(Fore.YELLOW + "4) -" + Fore.GREEN + " Search for a set by name")
        print(Fore.YELLOW + "5) -" + Fore.GREEN + " Generate current news (br)")
        print(Fore.YELLOW + "6) -" + Fore.GREEN + " Generate all new variants of the latest patch")
        print(Fore.YELLOW + "7) -" + Fore.GREEN + " Merge images")
        print(Fore.YELLOW + "8) -" + Fore.GREEN + " New Features")



    def inputs(self, x: Union[str, int, None]):
        newcosm = Commands(self)
        searchcosm = Commands(self)
        pak = Commands(self)
        merge = Commands(self)
        features = Commands(self)
        news = Commands(self)

        choices = {
            1: newcosm.NewCosmetics,
            2: searchcosm.SearchCosmetic,
            3: pak.paksearch,
            4: searchcosm.set,
            5: news.NewsGenerator,
            6: newcosm.NewVariants,
            7: merge.merge,
            8: features.feature
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
        
        
"""finished code"""