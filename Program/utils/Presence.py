import requests

from pypresence import Presence
from datetime import datetime

class RPC(Presence):
    def __init__(self):
        self.client_id = 968816560309436457 # if this client don't work, restart the program for fix the issue.
        self.start = datetime.now().timestamp()
        self.name = "Cosmetic Generator"
        self.access = "user_access"
        self.buttons = [
            {
                "label": "Download", 
                "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"
            },
            {
                "label": "Discord Server",
                "url": "https://discord.gg/X97U6PFGHc"
            }
        ]
        self.image = "rift"
        self.version = requests.get('https://fortnitecentral.gmatrixgames.ga/api/v1/aes').json()['version']
        self.details = f"Playing v{self.version}"

        super().__init__(
            client_id=self.client_id
        )

    def update(self, state: str = None):
        super().update(state=state, details=self.details, start=self.start, large_image=self.image, large_text=self.name, small_image=self.access, small_text="User Access", buttons=self.buttons)
