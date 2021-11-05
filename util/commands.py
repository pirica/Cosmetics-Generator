import colorama 
import time
import glob
import requests

from util.BaseIcon import BaseIcon
from util.deleter import deleter

from math import ceil, sqrt
from colorama import Fore
from PIL import Image

colorama.init(autoreset=True)

class Commands:
    def __init__(self, data):
        self.language = data.language
        self.searchlanguage = data.searchlanguage
        self.automerge = data.mergeauto
        self.twitter = data.twitter
        self.newtext = data.newcosmeticsText
        self.paktext = data.pakText

    def feature(self):
        print(Fore.RED + "---- NEW FEATURES ----")
        print(Fore.YELLOW + "[1]" + Fore.GREEN + "Added autopost to Twitter!")

    def NewCosmetics(self):
        print(Fore.GREEN + "Generating new cosmetics..")
        res = requests.get(
            f'https://fortnite-api.com/v2/cosmetics/br/new?language={self.language}'
        )
        responce = res.json()
        if responce.status_code == 200:
            responce = res.json()['data']['items']
            start = time.time()
            count = 1
            for data in responce:
                percentage = (count/len(responce)) * 100
                BaseIcon().main(data)
                print(Fore.BLUE + f"Generated image for {data['id']} -" + Fore.YELLOW + f" {count}/{len(responce)} - {round(percentage)}%")
                count += 1
            if self.automerge:
                print(Fore.BLUE + "Merging images...")
                datas = [Image.open(i) for i in glob.glob(f'cache/*.png')]
                    
                row_n = len(datas)
                rowslen = ceil(sqrt(row_n))
                columnslen = round(sqrt(row_n))

                mode = "RGB"
                px = 512
                rows = rowslen * px
                columns = columnslen * px
                image = Image.new(mode, (rows, columns))
                i = 0
                for card in datas:
                    image.paste(
                        card,
                        ((0 + ((i % rowslen) * card.width)),
                        (0 + ((i // rowslen) * card.height)))
                    )
                    i += 1
                image.save('images/newcosmetics.jpg')
                image.show()
                if self.twitter != False:
                    try:
                        self.twitter.update_with_media(
                            "images/newcosmetics.jpg",
                            status=self.newText
                        )
                    except Exception as exception:
                        print(Fore.RED + f"Failed to tweet the newcosmetics image!\n{exception}")
            print(Fore.GREEN + f"Generated in {round(time.time() - start, 2)} seconds")
            deleter()
        elif responce['status'] != 200:
            print(Fore.RED + f"[ERROR] The api return a {res['status']} error")


    def SearchCosmetic(self):
        print(Fore.GREEN + "What cosmetic do you want to grab?")
        ask = input('> ')
        res = requests.get(
            f'https://fortnite-api.com/v2/cosmetics/br/search?name={ask}&language={self.language}&searchLanguage={self.searchlanguage}'
        )
        if res.status_code == 200:
            responce = res.json()['data']
            start = time.time()
            image = BaseIcon().main(responce)
            print(Fore.BLUE + f"Generated image for {responce['id']}")
            print(Fore.GREEN + f"Generated in {round(time.time() - start, 2)} seconds")
            image.show()
        elif res.status_code == 404:
            print(Fore.RED + f"[ERROR] The cosmetic you search doesn't exist")
        else:
            print(Fore.RED + "Api down!")


    def paksearch(self):
        print(Fore.GREEN + "What number pak do you want to grab?")
        ask = input('>> ')
        res = requests.get(
            f'https://fortnite-api.com/v2/cosmetics/br/search/all?dynamicPakId={ask}&language={self.language}'
        )    
        if res.status_code == 200:               
            res = res.json()['data']
            start = time.time()
            count = 1
            for data in res:
                percentage = (count/len(res)) * 100
                BaseIcon().main(data)
                print(Fore.BLUE + f"Generated image for {data['id']} -" + Fore.YELLOW + f" {count}/{len(res)} - {round(percentage)}%")
                count += 1
            if self.automerge:
                print(Fore.BLUE + "Merging images...")
                datas = [Image.open(i) for i in glob.glob(f'cache/*.png')]
                    
                row_n = len(datas)
                rowslen = ceil(sqrt(row_n))
                columnslen = round(sqrt(row_n))

                mode = "RGB"
                px = 512
                rows = rowslen * px
                columns = columnslen * px
                image = Image.new(mode, (rows, columns))
                i = 0
                for card in datas:
                    image.paste(
                        card,
                        ((0 + ((i % rowslen) * card.width)),
                        (0 + ((i // rowslen) * card.height)))
                    )
                    i += 1
                image.save(f'images/pak {ask}.jpg')
                image.show()
                if self.twitter != False:
                    try:
                        self.twitter.update_with_media(
                            f"images/pak {ask}.jpg",
                            status=self.pakText
                        )
                    except Exception as exception:
                        print(Fore.RED + f"Failed to tweet the pak image!\n{exception}")
            print(Fore.GREEN + f"Generated in {round(time.time() - start, 2)} seconds")
            deleter()
        elif res.status_code != 200:
            print(Fore.RED + f"[ERROR] The api return a {res.status_code} error")

    
    def merge(self):
        print(Fore.BLUE + "Merging images..")
        datas = [Image.open(i) for i in glob.glob(f'cache/*.png')]
                
        row_n = len(datas)
        rowslen = ceil(sqrt(row_n))
        columnslen = round(sqrt(row_n))

        mode = "RGB"
        px = 512
        rows = rowslen * px
        columns = columnslen * px
        image = Image.new(mode, (rows, columns))
        i = 0
        for card in datas:
            image.paste(
                card,
                ((0 + ((i % rowslen) * card.width)),
                (0 + ((i // rowslen) * card.height)))
            )
            i += 1
        image.save('images/merge.jpg')
        image.show()