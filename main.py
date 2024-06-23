import asyncio
import os
import json
import sys
from Battle import Battle
from Pixelverse import UserPixel
from random import randint
from colorama import Fore, Style, init 
from time import sleep

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
clear()

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

async def main():
    try:
        init()
        user = UserPixel()
        battle = Battle()
        users = user.getUsers()
        stats = user.getStats()
        winRate = (stats['wins'] / stats['battlesCount']) * 100
        dailyRewards = user.getDailyRewards()
        claimDailyRewards = user.claimDailyRewards()
        
        print(f"👻 {Fore.CYAN+Style.BRIGHT}[ User ]\t\t: {Fore.RED+Style.BRIGHT}[ Username ] {users['username']}")
        print(f"👻 {Fore.CYAN+Style.BRIGHT}[ User ]\t\t: {Fore.RED+Style.BRIGHT}[ Balance ] {split_chunk(str(int(users['clicksCount'])))} Coins")
        print(f"👻 {Fore.YELLOW+Style.BRIGHT}[ User Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins ] {split_chunk(str(stats['wins']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Loses ] {split_chunk(str(stats['loses']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Battles Count ] {split_chunk(str(stats['battlesCount']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.WHITE+Style.BRIGHT}[ Winrate ] {winRate:.2f}%")
        print(f"👻 {Fore.YELLOW+Style.BRIGHT}[ User Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins Reward ] {split_chunk(str(stats['winsReward']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Loses Reward ] {split_chunk(str(stats['losesReward']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Total Earned ] {split_chunk(str(stats['winsReward'] + stats['losesReward']))}")
        user.claim()
        print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.BLUE+Style.BRIGHT}[ Total Claimed ] {split_chunk(str(dailyRewards['totalClaimed']))} Coins")
        print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.BLUE+Style.BRIGHT}[ Day ] {split_chunk(str(dailyRewards['day']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Reward Amount ] {split_chunk(str(dailyRewards['rewardAmount']))} Coins")
        print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.BLUE+Style.BRIGHT}[ Next Day ] {split_chunk(str(dailyRewards['nextDay']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Next Day Reward Amount ] {split_chunk(str(dailyRewards['nextDayRewardAmount']))} Coins")
        if dailyRewards['todaysRewardAvailable'] == True:
            print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Todays Reward Available ] Available")
            print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.GREEN+Style.BRIGHT}[ Claiming ] | [ Day ] {claimDailyRewards['day']} | [ Amount ] {claimDailyRewards['amount']}")
            user.claimDailyRewards()
        else:
            print(f"🗓️ {Fore.MAGENTA+Style.BRIGHT}[ Daily Reward ]\t: {Fore.RED+Style.BRIGHT}[ Todays Reward Available ] Not Available")

        print('')

        with open('./config.json', 'r') as config_file:
            config = json.load(config_file)
        
        await battle.connect()
        del battle

        print('')

        user.upgradePets(auto_upgrade=config['auto_upgrade'])
    except Exception as e:
        print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error ]\t: {e}")

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print(f"👋🏻 {Fore.RED+Style.BRIGHT}[ Dadah ]")
            sys.exit(0)
        except Exception as e:
            if UserPixel().isBroken():
                print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error ]\t: {e}")
                sleep(randint(5, 10)*5)
            else:
                print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error ]\t: {type(e).__name__} {e}")
                sleep(randint(5, 10))
        clear()