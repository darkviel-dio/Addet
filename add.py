'''
================SAIFALISEW1508=====================
Telegram members adding script
Coded by a kid- github.com/saifalisew1508
Apologies if anything in the code is dumb :)
Copy with credits
Enhanced with robust session persistence
FIXED: Allow editing resumed session settings
************************************************
'''

# import libraries
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError, 
    ChatAdminRequiredError, ChatWriteForbiddenError, UserBannedInChannelError, 
    UserAlreadyParticipantError, FloodWaitError)

from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import UserStatusRecently
import sys
import time
import random
from colorama import init, Fore
import os
import json
init()

# Define colors for console output
r = Fore.RED
lg = Fore.GREEN
n = Fore.RESET
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = f'{lg}[{w}i{lg}]{n}'
error = f'{lg}[{r}!{lg}]{n}'
success = f'{w}[{lg}*{w}]{n}'
INPUT = f'{lg}[{cy}~{lg}]{n}'
plus = f'{w}[{lg}+{w}]{n}'
minus = f'{w}[{lg}-{w}]{n}'

SESSION_FILE = 'session_state.json'

def banner():
    # Fancy logo
    b = [
    '░█████╗░██████╗░██████╗░███████╗██████╗░',
    '██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗',
    '███████║██║░░██║██║░░██║█████╗░░██████╔╝',
    '██╔══██║██║░░██║██║░░██║██╔══╝░░██╔══██╗',
    '██║░░██║██████╔╝██████╔╝███████╗██║░░██║',
    '╚═╝░░╚═╝╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print('Contact below address for get premium script')
    print(f'{lg}Version: {w}2.1{lg} | GitHub: {w}@saifalisew1508{n}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}@_Prince.Babu_{n}')

# Function to clear screen
def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Load accounts from accounts.json
def load_accounts():
    """Load all accounts from accounts.json"""
    if os.path.exists('accounts.json'):
        with open('accounts.json', 'r') as f:
            return json.load(f)
    return []

# ===== NEW: Session State Management =====
def save_session_state(state):
    """Save session state to JSON (more reliable than pickle)"""
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        print(f'{info}{lg} Session saved: {w}{SESSION_FILE}{n}')
    except Exception as e:
        print(f'{error}{r} Failed to save session: {e}{n}')

def load_session_state():
    """Load previous session state from JSON"""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                state = json.load(f)
            print(f'{info}{lg} Previous session found!{n}')
            return state
        except Exception as e:
            print(f'{error}{r} Failed to load session: {e}{n}')
            return None
    return None

def display_session_info(state):
    """Display saved session information (safe against missing keys)"""
    print(f'\n{cy}===== SAVED SESSION INFO ====={n}')
    print(f'{info}{lg} Accounts to use: {w}{state.get("number_of_accounts", "?")}{n}')
    print(f'{info}{lg} Group/Channel: {w}{state.get("group_link", "?")}{n}')
    print(f'{info}{lg} Target group: {w}{state.get("target_link", "?")}{n}')
    print(f'{info}{lg} Current index: {w}{state.get("member_index", 0)}{n}')
    print(f'{info}{lg} Active members only: {w}{state.get("active_members_only", False)}{n}')
    print(f'{info}{lg} Delay time: {w}{state.get("sleep_time", 30)}s{n}')
    if "timestamp" in state:
        print(f'{info}{lg} Saved at: {w}{state["timestamp"]}{n}')
    print(f'{cy}=============================={n}\n')
def edit_resume_settings(state, accounts_list):
    """Allow user to edit resumed settings before continuing"""
    print(f'\n{cy}===== EDIT SESSION SETTINGS ====={n}')
    
    # Menu to edit settings
    print(f'{info}{lg} Press Enter to keep current value, or type new value:')
    
    # Edit account range
    current_accs = state["number_of_accounts"]
    new_accs = input(f'{INPUT}{cy} Account range (e.g., 1-24, 24-3, or 23) [{w}{current_accs}{cy}]: {r}').strip()
    if new_accs:
        try:
            if '-' in new_accs:
                parts = new_accs.split('-')
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                if start > end:
                    selected = accounts_list[end:start+1][::-1]
                else:
                    selected = accounts_list[start:end+1]
                state["number_of_accounts"] = len(selected)
            else:
                account_num = int(new_accs)
                state["number_of_accounts"] = 1
            print(f'{success} Account range updated to {state["number_of_accounts"]} account(s)')
        except (ValueError, IndexError):
            print(f'{error} Invalid range, keeping current value')
    
    # Edit target group
    current_target = state["target_link"]
    new_target = input(f'{INPUT}{cy} Target group [{w}{current_target}{cy}]: {r}').strip()
    if new_target:
        state["target_link"] = new_target
        print(f'{success} Target group updated')
    
    # Edit source group
    current_source = state["group_link"]
    new_source = input(f'{INPUT}{cy} Source group to scrape [{w}{current_source}{cy}]: {r}').strip()
    if new_source:
        state["group_link"] = new_source
        print(f'{success} Source group updated')
    
    # Edit sleep time
    current_sleep = state["sleep_time"]
    new_sleep = input(f'{INPUT}{cy} Delay time in seconds [{w}{current_sleep}{cy}]: {r}').strip()
    if new_sleep:
        try:
            state["sleep_time"] = int(new_sleep)
            print(f'{success} Delay time updated')
        except ValueError:
            print(f'{error} Invalid number, keeping current value')
    
    # Edit active members filter
    current_active = state["active_members_only"]
    new_active = input(f'{INPUT}{cy} Add active members only? [{w}{"y" if current_active else "n"}{cy}]: {r}').strip().lower()
    if new_active in ['y', 'n']:
        state["active_members_only"] = (new_active == 'y')
        print(f'{success} Active members filter updated')
    
    # Reset member index to start from beginning if changing groups
    reset_index = input(f'{INPUT}{cy} Start from member 0? [y/n]: {r}').strip().lower()
    if reset_index == 'y':
        state["member_index"] = 0
        print(f'{success} Member index reset to 0')
    
    print(f'{cy}=============================={n}\n')
    return state
# ===== END: Session State Management =====

accounts = load_accounts()

# Create sessions and check for banned accounts
print('\n' + info + lg + ' Checking for banned accounts...' + n)
banned = []
for acc in accounts:
    phn = acc['phone']
    print(f'{plus}{grey} Checking {lg}{phn}')
    clnt = TelegramClient(
        f'sessions/{phn}', 
        3913940, 
        '9367a1c841e8bafb8cde158f809be37d',
        device_model=acc.get('device_model', 'Samsung Galaxy A10'),
        system_version=acc.get('system_version', 'Android 9.0.0'),
        app_version=acc.get('app_version', '8.0.0')
    )
    clnt.connect()
    if not clnt.is_user_authorized():
        try:
            clnt.send_code_request(phn)
            print('OK')
        except PhoneNumberBannedError:
            print(f'{error} {w}{phn} {r}is banned!{n}')
            banned.append(acc)
    clnt.disconnect()

for z in banned:
    accounts.remove(z)
    print(info + lg + ' Banned account removed[Remove permanently using manager.py]' + n)
    time.sleep(0.5)

# Save updated accounts
with open('accounts.json', 'w') as f:
    json.dump(accounts, f, indent=2)

print(f'{info} Sessions created!')
clr()
banner()

def exit_window():
    input(f'\n{cy} Press enter to exit...')
    clr()
    banner()
    sys.exit()

# Function to send message using all accounts
def send_message_all_accounts():
    message = input(f'\n{lg} [~] Enter the message to send: {r}')
    promotional_message = "This message was sent using mass DM tool GitHub.com/saifalisew1508/Telegram-Members-Adder"
    full_message = f"{message}\n\n{promotional_message}"
    for acc in accounts:
        phone = acc['phone']
        client = TelegramClient(
            f'sessions/{phone}', 
            3910389, 
            '9367a1c841e8bafb8cde158f809be37d',
            device_model=acc.get('device_model', 'Samsung Galaxy A10'),
            system_version=acc.get('system_version', 'Android 9.0.0'),
            app_version=acc.get('app_version', '8.0.0')
        )
        client.connect()
        if client.is_user_authorized():
            try:
                client.send_message("me", full_message)
                print(f'{lg}[+] Message sent from {phone}')
            except Exception as e:
                print(f'{r}[!] Failed to send message from {phone}: {e}')
        client.disconnect()
    input('\nPress enter to exit...')

# Function to join a group or channel using all accounts
def join_group_all_accounts():
    link = input(f'\n{lg} [~] Enter the group/channel link to join: {r}')
    for acc in accounts:
        phone = acc['phone']
        client = TelegramClient(
            f'sessions/{phone}', 
            3910389, 
            '86f861352f0ab76a251866059a6adbd6',
            device_model=acc.get('device_model', 'Samsung Galaxy A10'),
            system_version=acc.get('system_version', 'Android 9.0.0'),
            app_version=acc.get('app_version', '8.0.0')
        )
        client.connect()
        if client.is_user_authorized():
            try:
                client(JoinChannelRequest(link))
                print(f'{lg}[+] Joined group/channel from {phone}')
            except Exception as e:
                print(f'{r}[!] Failed to join from {phone}: {e}')
        client.disconnect()

def leave_group_all_accounts():
    link = input(f'\n{lg} [~] Enter the group/channel link to leave: {r}')
    for acc in accounts:
        phone = acc['phone']
        client = TelegramClient(
            f'sessions/{phone}', 
            3910389, 
            '86f861352f0ab76a251866059a6adbd6',
            device_model=acc.get('device_model', 'Samsung Galaxy A10'),
            system_version=acc.get('system_version', 'Android 9.0.0'),
            app_version=acc.get('app_version', '8.0.0')
        )
        client.connect()
        if client.is_user_authorized():
            try:
                client(LeaveChannelRequest(link))
                print(f'{lg}[+] Left group/channel from {phone}')
            except Exception as e:
                print(f'{r}[!] Failed to leave from {phone}: {e}')
        client.disconnect()

def report_group_all_accounts():
    link = input(f'\n{lg} [~] Enter the group/channel link to report: {r}')
    reason = input(f'\n{lg} [~] Enter report reason: {r}')
    for acc in accounts:
        phone = acc['phone']
        client = TelegramClient(
            f'sessions/{phone}', 
            3910389, 
            '86f861352f0ab76a251866059a6adbd6',
            device_model=acc.get('device_model', 'Samsung Galaxy A10'),
            system_version=acc.get('system_version', 'Android 9.0.0'),
            app_version=acc.get('app_version', '8.0.0')
        )
        client.connect()
        if client.is_user_authorized():
            try:
                client(ReportRequest(link, reason=reason))
                print(f'{lg}[+] Reported group/channel from {phone}')
            except Exception as e:
                print(f'{r}[!] Failed to report from {phone}: {e}')
        client.disconnect()

def add_hidden_members_from_group():
    # Placeholder for hidden members function (not fully implemented in original)
    group_link = input(f'\n{lg} [~] Enter group link to extract hidden members: {r}')
    target_link = input(f'{lg} [~] Enter target group to add members: {r}')
    print(f'{info}{lg} This feature requires advanced scraping')

def get_account_range():
    """Prompt user to select account range flexibly (e.g., 1-24, 24-3, or just 23)"""
    print(f'{info}{lg} Total {w}{len(accounts)}{lg} account(s) available')
    range_input = input(f'{INPUT}{cy} Enter account range (e.g., 1-24, 24-3, or single number 23): {r}').strip()
    
    try:
        if '-' in range_input:
            parts = range_input.split('-')
            start = int(parts[0].strip())
            end = int(parts[1].strip())
            # Handle reverse range (e.g., 24-3 means from 24 down to 3)
            if start > end:
                to_use = accounts[end:start+1][::-1]  # Reverse the slice
            else:
                to_use = accounts[start:end+1]
        else:
            # Single account number
            account_num = int(range_input)
            to_use = [accounts[account_num]]
        
        if len(to_use) == 0:
            print(f'{error} Invalid range. Using all accounts.')
            to_use = accounts
        
        return to_use, len(to_use)
    except (ValueError, IndexError):
        print(f'{error} Invalid input. Using all accounts.')
        return accounts, len(accounts)

# ===== LOAD PREVIOUS SESSION IF EXISTS =====
previous_session = load_session_state()

if previous_session:
    display_session_info(previous_session)
    resume_choice = input(f'{INPUT}{cy} Resume previous session? [y/n]: {r}').strip().lower()
    
    if resume_choice == 'y':
        # ===== NEW: Allow editing before resuming =====
        edit_choice = input(f'{INPUT}{cy} Edit settings before resuming? [y/n]: {r}').strip().lower()
        if edit_choice == 'y':
            previous_session = edit_resume_settings(previous_session, accounts)
        # ===== END: EDIT CHOICE =====
        
        number_of_accs = previous_session["number_of_accounts"]
        to_use = accounts[:number_of_accs]
        scraped_grp = previous_session["group_link"]
        target = previous_session["target_link"]
        index = previous_session["member_index"]
        status_choice = 'y' if previous_session["active_members_only"] else 'n'
        sleep_time = previous_session["sleep_time"]
        choice = 0  # Assuming it's adding members
    else:
        os.remove(SESSION_FILE)
        print(f'{info}{lg} Session removed. Starting fresh...{n}')
        to_use, number_of_accs = get_account_range()
else:
    to_use, number_of_accs = get_account_range()

if 'to_use' not in locals() or 'number_of_accs' not in locals():
    to_use, number_of_accs = get_account_range()

print(f'{info}{lg} Selected {w}{number_of_accs}{lg} account(s)')
print(f'{info}{cy} Choose an option{lg}')
print(f'{cy}[0]{lg} Add members to group')
print(f'{cy}[1]{lg} Send message using all accounts')
print(f'{cy}[2]{lg} Join a group/channel using all accounts')
print(f'{cy}[3]{lg} Leave a group/channel using all accounts')
print(f'{cy}[4]{lg} Report a group/channel using all accounts')
print(f'{cy}[5]{lg} Add hidden members from group using their messages')

if 'choice' not in locals():
    choice = int(input(f'{INPUT}{cy} Enter choice: {r}'))

if choice == 0:
    if 'target' not in locals():
        target = input(f'{INPUT}{cy} Enter group url link: {r}')
    if 'scraped_grp' not in locals():
        scraped_grp = input(f'{INPUT}{cy} Public/Private group url link to scrape members: {r}')
    if 'index' not in locals():
        index = 0
    if 'status_choice' not in locals():
        print(f'{grey}_'*50)
        status_choice = input(f'{INPUT}{cy} Do you wanna add active members?[y/n]: {r}')
    if 'sleep_time' not in locals():
        sleep_time = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None, i suggest enter 30 to add members properly{w}]: {r}'))
    
    # ===== SAVE SESSION STATE AT START =====
    session_state = {
        "number_of_accounts": number_of_accs,
        "group_link": scraped_grp,
        "target_link": target,
        "member_index": index,
        "active_members_only": status_choice == 'y',
        "sleep_time": sleep_time,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    save_session_state(session_state)
    # ===== END: SAVE SESSION STATE =====
    
    print(f'{info}{lg} Joining group from {w}{number_of_accs} accounts...')
    print(f'{grey}-'*50)
    print(f'{success}{lg} -- Adding members from {w}{len(to_use)}{lg} account(s) --')

    adding_status = 0
    approx_members_count = 0
    for acc in to_use:
        stop = index + 60
        c = TelegramClient(
            f'sessions/{acc["phone"]}', 
            3910389, 
            '86f861352f0ab76a251866059a6adbd6',
            device_model=acc.get('device_model', 'Samsung Galaxy A10'),
            system_version=acc.get('system_version', 'Android 9.0.0'),
            app_version=acc.get('app_version', '8.0.0')
        )
        print(f'{plus}{grey} User: {cy}{acc["phone"]}{lg} -- {cy}Starting session... ')
        c.start(acc["phone"])
        acc_name = c.get_me().first_name
        try:
            if '/joinchat/' in scraped_grp:
                g_hash = scraped_grp.split('/joinchat/')[1]
                try:
                    c(ImportChatInviteRequest(g_hash))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
                except UserAlreadyParticipantError:
                    pass
            else:
                c(JoinChannelRequest(scraped_grp))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
            scraped_grp_entity = c.get_entity(scraped_grp)
            if choice == 0:
                c(JoinChannelRequest(target))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
                target_entity = c.get_entity(target)
                target_details = InputPeerChannel(target_entity.id, target_entity.access_hash)
            else:
                try:
                    grp_hash = target.split('/joinchat/')[1]
                    c(ImportChatInviteRequest(grp_hash))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
                except UserAlreadyParticipantError:
                    pass
                target_entity = c.get_entity(target)
                target_details = target_entity
        except Exception as e:
            print(f'{error}{r} User: {cy}{acc_name}{lg} -- Failed to join group')
            print(f'{error} {r}{e}')
            continue

        print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}Retrieving entities...')
        c.get_dialogs()
        try:
            members = c.get_participants(scraped_grp_entity, aggressive=False)
        except Exception as e:
            print(f'{error}{r} Couldn\'t scrape members')
            print(f'{error}{r} {e}')
            continue

        approx_members_count = len(members)
        if approx_members_count == 0:
            print(f'{error}{lg} No members to add!')
            continue

        print(f'{info}{lg} Start: {w}{index}')
        adding_status = 0
        peer_flood_status = 0
        for user in members[index:stop]:
            index += 1
            # ===== UPDATE SESSION AFTER EACH USER =====
            session_state["member_index"] = index
            save_session_state(session_state)
            # ===== END: UPDATE SESSION =====
            
            if peer_flood_status == 10:
                print(f'{error}{r} Too many Peer Flood Errors! Closing session...')
                break
            try:
                if choice == 0:
                    c(InviteToChannelRequest(target_details, [user]))
                else:
                    c(AddChatUserRequest(target_details.id, user, 42))
                user_id = user.first_name
                target_title = target_entity.title
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}{user_id} {lg}--> {cy}{target_title}')
                adding_status += 1
                print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time} {lg}second(s)')
                time.sleep(sleep_time)
            except UserPrivacyRestrictedError:
                print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User Privacy Restricted Error')
                continue
            except PeerFloodError:
                print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error.')
                peer_flood_status += 1
                continue
            except ChatWriteForbiddenError:
                print(f'{error}{r} Can\'t add to group. Contact group admin to enable members adding')
                if index < approx_members_count:
                    pass  # Session already saved
                exit_window()
            except UserBannedInChannelError:
                print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Banned from writing in groups')
                break
            except ChatAdminRequiredError:
                print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Chat Admin rights needed to add')
                break
            except UserAlreadyParticipantError:
                print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User is already a participant')
                continue
            except FloodWaitError as e:
                print(f'{error}{r} {e}')
                break
            except ValueError:
                print(f'{error}{r} Error in Entity')
                continue
            except KeyboardInterrupt:
                print(f'{error}{r} ---- Adding Terminated ----')
                print(f'{info}{lg} Session preserved for resume!{n}')
                exit_window()
            except Exception as e:
                print(f'{error} {e}')
                continue

    if adding_status != 0:
        print(f"\n{info}{lg} Adding session ended")
    try:
        if index >= approx_members_count:
            # All members added, clean up session file
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
                print(f'{info}{lg} Session completed and cleared!{n}')
        exit_window()
    except:
        exit_window()
elif choice == 1:
    send_message_all_accounts()
elif choice == 2:
    join_group_all_accounts()
elif choice == 3:
    leave_group_all_accounts()
elif choice == 4:
    report_group_all_accounts()
elif choice == 5:
    add_hidden_members_from_group()
