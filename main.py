import asyncio
import os
import json
import sys
from Battle import Battle
from Pixel import Pixel
from colorama import Fore, Style, init

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

async def main():
    init(autoreset=True)
    user = Pixel()
    users = user.getUsers()
    stats = user.getStats()
    battle = Battle()
    
    print(f"👻 {Fore.CYAN+Style.BRIGHT}[ User ]\t\t: {Fore.RED+Style.BRIGHT}[ Username ] {users['username']}")
    print(f"👻 {Fore.CYAN+Style.BRIGHT}[ User ]\t\t: {Fore.RED+Style.BRIGHT}[ Balance ] {split_chunk(str(int(users['clicksCount'])))} Coins")
    print(f"👻 {Fore.YELLOW+Style.BRIGHT}[ User Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins ] {split_chunk(str(stats['wins']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Loses ] {split_chunk(str(stats['loses']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Battles Count ] {split_chunk(str(stats['battlesCount']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.WHITE+Style.BRIGHT}[ Winrate ] {((stats['wins'] / stats['battlesCount']) * 100 ):.2f}%")
    print(f"👻 {Fore.YELLOW+Style.BRIGHT}[ User Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins Reward ] {split_chunk(str(stats['winsReward']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Loses Reward ] {split_chunk(str(stats['losesReward']))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Total Earned ] {split_chunk(str(stats['winsReward'] + stats['losesReward']))}")
    print(f"👻 {Fore.YELLOW+Style.BRIGHT}[ Fight Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins ] {split_chunk(str(battle.wins))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Loses ] {split_chunk(str(battle.loses))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Battles Count ] {split_chunk(str(battle.wins + battle.loses))} {Fore.YELLOW+Style.BRIGHT}| {Fore.WHITE+Style.BRIGHT}[ Winrate ] {battle.winRate:.2f}%")
    print(f"👻 {Fore.YELLOW+Style.BRIGHT}[ Fight Stats ]\t: {Fore.GREEN+Style.BRIGHT}[ Wins Reward ] {split_chunk(str(battle.rewardWins))} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Loses Reward ] {split_chunk(str(battle.rewardLoses))} {Fore.YELLOW+Style.BRIGHT}| {Fore.RED+Style.BRIGHT}[ Total Earned ] {split_chunk(str(battle.rewardWins + battle.rewardLoses))}")
    user.claim()
    user.dailyRewards(auto_daily_rewards=config['auto_daily_rewards'])
    user.upgradePets(auto_upgrade_pets=config['auto_upgrade_pets'])
    
    await battle.connect()
    del battle

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error ]\t\t: {type(e).__name__} {e}")
        clear()