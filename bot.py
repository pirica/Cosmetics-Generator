"""Program created by @djlorenzouasset on Github all right are reserved"""

try:
    import tkinter as tk
    import tkinter.messagebox
    import json
    import colorama
    import os
    import time    
    import webbrowser

    from colorama import Fore
    from typing import Union

    from util.error import NoDigit
    from util.commands import Commands
    from util.twitter import Twitter
except ModuleNotFoundError as e:
    print(Fore.RED + "Error: " + e)

window = tk.Tk()
window.wm_withdraw()

colorama.init(autoreset=True)

class main:
    def __init__(self):

        try:
            m = tkinter.messagebox.showinfo(title="Cosmetics Generator - Made by ᴅᴊʟᴏʀ3xᴢo", message=f"Hey {os.environ['username']}!\nRemember that you can follow me on Twitter (by clicking the 'ok' button below) and leave a star on Github!")
            if m == True:
                webbrowser.open_new('https://twitter.com/djlorenzouasset')
            else:
                webbrowser.open_new('https://twitter.com/djlorenzouasset')
            print(Fore.GREEN + "Loading settings..")
            config = json.loads(open("config.json").read()) # load configurations
            self.BoxIn = config.get('BoxIn')
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
        print(Fore.GREEN + "- - - - - MENU - - - - -")
        print("")
        print(Fore.YELLOW + "(1)" + Fore.GREEN + " - Generate newcosmetics")
        print(Fore.YELLOW + "(2)" + Fore.GREEN + " - Search for a cosmetics")
        print(Fore.YELLOW + "(3)" + Fore.GREEN + " - Search for a pak")
        print(Fore.YELLOW + "(4)" + Fore.GREEN + " - Search for a set")
        print(Fore.YELLOW + "(5)" + Fore.GREEN + " - Generate all new variants")
        print(Fore.YELLOW + "(6)" + Fore.GREEN + " - Merge images in cache folder")
        print(Fore.YELLOW + "(7)" + Fore.GREEN + " - New Features")



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
            4: searchcosm.set,
            5: newcosm.NewVariants,
            6: merge.merge,
            7: features.feature
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
