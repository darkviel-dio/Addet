
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import json, os, random
from colorama import init, Fore
from time import sleep

init()

# Define colors for console output
n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')

# Common cheap phones used in Africa
CHEAP_PHONES = [
    'itel A16', 'itel A25', 'itel P36', 'itel S15',
    'Tecno Spark 4', 'Tecno Spark 5', 'Tecno Spark 6', 'Tecno Spark 7',
    'Tecno Camon 12', 'Tecno Camon 15', 'Tecno Camon 16',
    'Tecno Pop 4', 'Tecno Pop 5', 'Tecno Pop 6',
    'Infinix Hot 8', 'Infinix Hot 9', 'Infinix Hot 10', 'Infinix Hot 11',
    'Infinix Smart 4', 'Infinix Smart 5', 'Infinix Smart 6',
    'Samsung Galaxy A10', 'Samsung Galaxy A20', 'Samsung Galaxy A30',
    'Samsung Galaxy A01', 'Samsung Galaxy A02s', 'Samsung Galaxy A12',
    'Xiaomi Redmi 9', 'Xiaomi Redmi 9A', 'Xiaomi Redmi 10',
    'Nokia 2.3', 'Nokia 3.4', 'Nokia 4.2', 'Nokia 5.3',
    'Huawei Y5', 'Huawei Y6', 'Huawei Y7', 'Huawei Y9',
    'Oppo A15', 'Oppo A31', 'Oppo A52', 'Oppo A53',
    'Realme C11', 'Realme C15', 'Realme C21', 'Realme C25',
]

# Telegram versions
TELEGRAM_VERSIONS = [
    '7.5.0', '7.6.0', '7.7.0', '7.8.0', '7.9.0',
    '8.0.0', '8.1.0', '8.2.0', '8.3.0', '8.4.0',
    '8.5.0', '8.6.0', '8.7.0', '8.8.0', '8.9.0',
    '9.0.0', '9.1.0', '9.2.0', '9.3.0', '9.4.0',
    '9.5.0', '9.6.0', '9.7.0', '9.8.0', '9.9.0',
]

# Android versions (older ones common in Africa)
ANDROID_VERSIONS = [
    '6.0.1', '7.0', '7.1.1', '7.1.2',
    '8.0.0', '8.1.0', '9.0.0', '10.0.0', '11.0.0', '12.0.0'
]

def get_random_device_info():
    """Generate random device info for login"""
    phone = random.choice(CHEAP_PHONES)
    tg_version = random.choice(TELEGRAM_VERSIONS)
    android = random.choice(ANDROID_VERSIONS)
    return {
        'device_model': phone,
        'system_version': f'Android {android}',
        'app_version': tg_version
    }

def banner():
    import random
    b = [
    '░██████╗███████╗████████╗██╗░░░██╗██████╗░',
    '██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗',
    '╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝',
    '░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░',
    '██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░',
    '╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print('Contact below address for get premium script')
    print(f'{lg}Version: {w}2.6.82{lg} | GitHub: {w}@saifalisew1508{n}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}www.instagram.com/saifaliopp{n}')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_accounts():
    """Load all accounts from accounts.json"""
    if os.path.exists('accounts.json'):
        with open('accounts.json', 'r') as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    """Save accounts to accounts.json"""
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=2)

def add_new_accounts():
    new_accs = []
    existing_accounts = load_accounts()
    existing_numbers = {acc['phone'] for acc in existing_accounts}
    
    number_to_add = int(input(f'\n{lg} [~] Enter How Many Accounts You Want To Add: {r}'))
    for _ in range(number_to_add):
        phone_number = str(input(f'\n{lg} [~] Enter Phone Number With Country Code: {r}'))
        parsed_number = ''.join(phone_number.split())
        
        if parsed_number in existing_numbers:
            print(f'{r}[!] {parsed_number} already exists, skipping...{n}')
            continue
        
        # Generate device info for this account
        device_info = get_random_device_info()
        new_accs.append({
            'phone': parsed_number,
            'device_model': device_info['device_model'],
            'system_version': device_info['system_version'],
            'app_version': device_info['app_version']
        })
        existing_numbers.add(parsed_number)
    
    if not new_accs:
        print(f'{r}[!] No new accounts to add{n}')
        input(f'\n Press enter to goto main menu...')
        return
    
    all_accounts = existing_accounts + new_accs
    save_accounts(all_accounts)
    
    print(f'\n{lg} [i] Saved all accounts in accounts.json')
    clr()
    print(f'\n{lg} [*] Logging in from new accounts\n')
    for acc in new_accs:
        phone = acc['phone']
        print(f'{lg}[+] Logging in with {acc["device_model"]} ({acc["system_version"]}, Telegram {acc["app_version"]})')
        
        c = TelegramClient(
            f'sessions/{phone}', 
            8027196, 
            '9b70b20efd67e9b99edc395d78407cfa',
            device_model=acc['device_model'],
            system_version=acc['system_version'],
            app_version=acc['app_version']
        )
        c.start(phone=phone)
        print(f'{lg}[+] Login successful for {phone}')
        c.disconnect()
    input(f'\n Press enter to goto main menu...')

def filter_banned_accounts():
    accounts = load_accounts()
    
    if not accounts:
        print(f'{r}[!] There are no accounts! Please add some and retry')
        sleep(3)
    else:
        banned_accs = []
        for acc in accounts:
            phone = acc['phone']
            print(f'{lg}[*] Checking {phone} with {acc["device_model"]} ({acc["system_version"]}, Telegram {acc["app_version"]})')
            
            client = TelegramClient(
                f'sessions/{phone}', 
                8027196, 
                '9b70b20efd67e9b99edc395d78407cfa',
                device_model=acc['device_model'],
                system_version=acc['system_version'],
                app_version=acc['app_version']
            )
            client.start(phone=phone)
            client.connect()
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    print(f'{lg}[+] {phone} is not banned{n}')
                except PhoneNumberBannedError:
                    print(r + phone + ' is banned!' + n)
                    banned_accs.append(acc)
            client.disconnect()
        
        if not banned_accs:
            print(f'{lg}Congrats! No banned accounts')
        else:
            for m in banned_accs:
                accounts.remove(m)
            save_accounts(accounts)
            print(f'{lg}[i] All banned accounts removed{n}')
        input('\nPress enter to goto main menu...')

def delete_specific_account():
    accs = load_accounts()
    
    if not accs:
        print(f'{r}[!] No accounts to delete{n}')
        input('\nPress enter to goto main menu...')
        return
    
    print(f'{lg}[i] Choose an account to delete\n')
    for i, acc in enumerate(accs):
        print(f'{lg}[{i}] {acc["phone"]}{n}')
    index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
    phone = accs[index]['phone']
    session_file = f'{phone}.session'
    if os.name == 'nt':
        os.system(f'del sessions\\{session_file}')
    else:
        os.system(f'rm sessions/{session_file}')
    del accs[index]
    save_accounts(accs)
    print(f'\n{lg}[+] Account Deleted{n}')
    input(f'\nPress enter to goto main menu...')

def update_script():
    print(f'\n{lg}[i] Checking for updates...')
    try:
        version = requests.get('https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/version.txt')
    except:
        print(f'{r} You are not connected to the internet')
        print(f'{r} Please connect to the internet and retry')
        exit()
    if float(version.text) > 2.0:
        prompt = str(input(f'{lg}[~] Update available[Version {version.text}]. Download?[y/n]: {r}'))
        if prompt in {'y', 'yes', 'Y'}:
            print(f'{lg}[i] Downloading updates...')
            if os.name == 'nt':
                os.system('del add.py')
                os.system('del manager.py')
            else:
                os.system('rm add.py')
                os.system('rm manager.py')
            os.system('curl -l -O https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/add.py')
            os.system('curl -l -O https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/manager.py')
            print(f'{lg}[*] Updated to version: {version.text}')
            input('Press enter to exit...')
            exit()
        else:
            print(f'{lg}[!] Update aborted.')
            input('Press enter to goto main menu...')
    else:
        print(f'{lg}[i] Your Telegram-Members-Adder is already up to date')
        input('Press enter to goto main menu...')

def display_all_accounts():
    accs = load_accounts()
    
    if not accs:
        print(f'{r}[!] No accounts stored{n}')
        input('\nPress enter to goto main menu')
        return
    
    print(f'\n{cy}')
    print(f'\tList Of Phone Numbers Are')
    print('==========================================================')
    for acc in accs:
        print(f'\t{acc["phone"]} - {acc["device_model"]}')
    print('==========================================================')
    input('\nPress enter to goto main menu')

while True:
    clr()
    banner()
    print(f'{lg}[1] Add new accounts{n}')
    print(f'{lg}[2] Filter all banned accounts{n}')
    print(f'{lg}[3] Delete specific accounts{n}')
    print(f'{lg}[4] Update your Script{n}')
    print(f'{lg}[5] Display All Accounts{n}')
    print(f'{lg}[6] Quit{n}')
    a = int(input('\nEnter your choice: '))
    if a == 1:
        add_new_accounts()
    elif a == 2:
        filter_banned_accounts()
    elif a == 3:
        delete_specific_account()
    elif a == 4:
        update_script()
    elif a == 5:
        display_all_accounts()
    elif a == 6:
        clr()
        banner()
        exit()