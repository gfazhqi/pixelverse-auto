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
            self.bot.send_message(chat_id=self.chat_id)
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ JSONDecodeError getUsers() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ RequestException getUsers() ]\t: {e}")

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

    def upgradePets(self, auto_upgrade_pets: bool):
        url = "https://api-clicker.pixelverse.xyz/api/pets"
        try:
            data = self.getUsers()
            req = requests.get(url, headers=self.headers)
            pets = req.json()['data']
            for pet in pets:
                if auto_upgrade_pets:
                    if pet['userPet']['level'] >= 39:
                        print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Is Max Level")
                    else:
                        if data['clicksCount'] >= pet['userPet']['levelUpPrice']:
                            self.upgrade(pet['userPet']['id'])
                            print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: [ {pet['name']} ] Success Level Up")
                        else:
                            print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: Not Enough Coins To Upgrade [ {pet['name']} ] {(split_chunk(str(int(pet['userPet']['levelUpPrice'] - data['clicksCount']))))} Coins Remaining")
                else:
                    print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Pets ]\t\t: Auto Upgrade Is `false` (Make It `true` In config.json If You Want Auto Upgrade Pets)")
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
        except json.JSONDecodeError:
            return
        except requests.RequestException:
            return

    def claimDailyRewards(self):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards/claim"
        try:
            req = requests.post(url, headers=self.headers)
            req.raise_for_status()
            return req.json()
        except json.JSONDecodeError:
            return
        except requests.RequestException:
            return

    def dailyRewards(self, auto_daily_rewards: bool):
        url = "https://api-clicker.pixelverse.xyz/api/daily-rewards"
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            claimDailyRewards = self.claimDailyRewards()
            dailyRewards = req.json()
            if auto_daily_rewards:
                if dailyRewards['todaysRewardAvailable'] == True:
                    print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Todays Reward Available ] Available")
                    print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Claiming ] | [ Day ] {claimDailyRewards['day']} | [ Amount ] {claimDailyRewards['amount']}")
                    self.claimDailyRewards()
                else:
                    print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.RED+Style.BRIGHT}[ Todays Reward Available ] Not Available")
                    print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.BLUE+Style.BRIGHT}[ Total Claimed ] {split_chunk(str(dailyRewards['totalClaimed']))} Coins")
                    print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.BLUE+Style.BRIGHT}[ Day ] {split_chunk(str(dailyRewards['day']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Reward Amount ] {split_chunk(str(dailyRewards['rewardAmount']))} Coins")
                    print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.BLUE+Style.BRIGHT}[ Next Day ] {split_chunk(str(dailyRewards['nextDay']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Next Day Reward Amount ] {split_chunk(str(dailyRewards['nextDayRewardAmount']))} Coins")
            else:
                print(f"🐈 {Fore.CYAN+Style.BRIGHT}[ Daily Reward ]\t\t: Auto Daily Rewards `false` (Make It `true` In config.json If You Want Auto Daily Rewards)")
        except json.JSONDecodeError as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ JSONDecodeError getDailyRewards() ]\t: {e}")
        except requests.RequestException as e:
            return print(f"🍓 {Fore.RED+Style.BRIGHT}[ RequestException getDailyRewards() ]\t: {e}")