import json
import colorama 
import os

from PIL import Image
from colorama import Fore
from util.error import NoDigit
from util.commands import Commands
from typing import Union

colorama.init(autoreset=True)

class main:
    def __init__(self):

        try:
            config = json.loads(open("config.json").read()) # load configurations

            self.language = config.get('language')
            self.searchlanguage = config.get('searchLanguage')         
            self.mergeauto = config.get('mergeauto')
            
        except Exception as e:
            print(Fore.RED + f"{e}")
        except FileNotFoundError as e:
            print(Fore.RED + f"{e}")


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


    def inputs(self, x: Union[str, int, None]):
        newcosm = Commands(self)
        searchcosm = Commands(self)
        pak = Commands(self)
        merge = Commands(self)

        choices = {
            1: newcosm.NewCosmetics,
            2: searchcosm.SearchCosmetic,
            3: pak.paksearch,
            4: merge.merge
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
