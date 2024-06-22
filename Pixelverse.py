import json
import requests
from colorama import Fore, Style
from datetime import datetime, timezone

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

class UserPixel:
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
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error getUsers() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error getUsers() ]\t: {e}")

    def getStats(self):
        url = "https://api-clicker.pixelverse.xyz/api/battles/my/stats"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error getStats() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error getStats() ]\t: {e}")

    def upgrade(self, petId: str):
        url = f"https://api-clicker.pixelverse.xyz/api/pets/user-pets/{petId}/level-up"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error upgrade() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error upgrade() ]\t: {e}")

    def upgradePets(self, auto_upgrade: bool):
        url = "https://api-clicker.pixelverse.xyz/api/pets"
        try:
            data = self.getUsers()
            req = requests.get(url, headers=self.headers)
            pets = req.json()['data']
            for pet in pets:
                if auto_upgrade:
                    if pet['userPet']['isMaxLevel'] == True:
                        print(f"🐈 {Fore.MAGENTA+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Is Max Level")
                    else:
                        if data['clicksCount'] >= pet['userPet']['levelUpPrice']:
                            self.upgrade(pet['userPet']['id'])
                            print(f"🐈 {Fore.MAGENTA+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Success Level Up")
                        else:
                            print(f"🐈 {Fore.MAGENTA+Style.BRIGHT}[ Pets ]\t\t: Not Enough Coins To Upgrade [ {pet['name']} ] {(split_chunk(str(int(pet['userPet']['levelUpPrice'] - data['clicksCount']))))} Coins Remaining")
                else:
                    print(f"🐈 {Fore.MAGENTA+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Can Upgrade")
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error upgradePets() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error upgradePets() ]\t: {e}")

    def claim(self):
        url = "https://api-clicker.pixelverse.xyz/api/mining/claim"
        try:
            req = requests.post(url, headers=self.headers)
            req.raise_for_status()
            data = req.json()
            nextFullRestorationDate = datetime.strptime(data['nextFullRestorationDate'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            print(f"🪙 {Fore.CYAN+Style.BRIGHT}[ Claim ]\t\t: {Fore.YELLOW+Style.BRIGHT}[ Max Available ] {split_chunk(str(int(data['maxAvailable'])))}")
            print(f"🪙 {Fore.CYAN+Style.BRIGHT}[ Claim ]\t\t: {Fore.YELLOW+Style.BRIGHT}[ Minimum Amount For Claim ] {split_chunk(str(int(data['minAmountForClaim'])))}")
            print(f"🪙 {Fore.CYAN+Style.BRIGHT}[ Claim ]\t\t: {Fore.YELLOW+Style.BRIGHT}[ Next Full Restoration Date ] {nextFullRestorationDate}")
            print(f"🪙 {Fore.CYAN+Style.BRIGHT}[ Claim ]\t\t: {Fore.YELLOW+Style.BRIGHT}[ Claimed Amount ] {split_chunk(str(int(data['claimedAmount'])))}")
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error claim() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error claim() ]\t: {e}")

    def getDailyRewards(self):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error getDailyRewards() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error getDailyRewards() ]\t: {e}")

    def claimDailyRewards(self):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards/claim"
        try:
            req = requests.post(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error claimDailyRewards() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error claimDailyRewards() ]\t: {e}")

    def isBroken(self):
        url = "https://api-clicker.pixelverse.xyz/api/tasks/my"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error isBroken() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error isBroken() ]\t: {e}")