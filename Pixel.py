import json
import requests
from colorama import Fore, Style

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

class Pixel:
    def __init__(self):
        with open('config.json', 'r') as file:
            self.config = json.load(file)
        
        self.headers = {
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "api-clicker.pixelverse.xyz",
            "If-None-Match": 'W/"29b-JPcgLG/Nvfd8KEVQN/lMKfPaHpQ"',
            "initData": self.config['initData'],
            "Origin": "https://sexyzbot.pxlvrs.io",
            "Priority": "u=3, i",
            "Referer": "https://sexyzbot.pxlvrs.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "secret": self.config['secret'],
            "tg-id": self.config['tgId'],
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
        }

    def getUsers(self):
        url = "https://api-clicker.pixelverse.xyz/api/users"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ JSONDecodeError getUsers() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ RequestException getUsers() ]\t: {e}")

    def getStats(self):
        url = "https://api-clicker.pixelverse.xyz/api/battles/my/stats"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ JSONDecodeError getStats() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ RequestException getStats() ]\t: {e}")

    def upgrade(self, petId: str):
        url = f"https://api-clicker.pixelverse.xyz/api/pets/user-pets/{petId}/level-up"
        try:
            req = requests.post(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return
        except requests.RequestException as e:
            return

    def upgradePets(self, auto_upgrade: bool):
        url = "https://api-clicker.pixelverse.xyz/api/pets"
        try:
            data = self.getUsers()
            req = requests.get(url, headers=self.headers)
            pets = req.json()['data']
            for pet in pets:
                if auto_upgrade:
                    if pet['userPet']['isMaxLevel'] == True:
                        print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Is Max Level")
                    else:
                        if data['clicksCount'] >= pet['userPet']['levelUpPrice']:
                            self.upgrade(pet['userPet']['id'])
                            print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Success Level Up")
                        else:
                            print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: Not Enough Coins To Upgrade [ {pet['name']} ] {(split_chunk(str(int(pet['userPet']['levelUpPrice'] - data['clicksCount']))))} Coins Remaining")
                else:
                    print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Can Upgrade")
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ JSONDecodeError upgradePets() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ RequestException upgradePets() ]\t: {e}")

    def claim(self):
        url = "https://api-clicker.pixelverse.xyz/api/mining/claim"
        try:
            req = requests.post(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return
        except requests.RequestException as e:
            return

    def getDailyRewards(self):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ JSONDecodeError getDailyRewards() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ RequestException getDailyRewards() ]\t: {e}")

    def claimDailyRewards(self):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards/claim"
        try:
            req = requests.post(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return
        except requests.RequestException as e:
            return

    def isBroken(self):
        url = "https://api-clicker.pixelverse.xyz/api/tasks/my"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ JSONDecodeError isBroken() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ RequestException isBroken() ]\t: {e}")