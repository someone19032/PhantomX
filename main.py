import os
import sys
import time
import json
import requests
from colorama import Fore, Style, init

init(autoreset=True)

SESSION_FILE = "session.json"
SENT_MESSAGES_FILE = "sent_messages.json"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_session(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return {}

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def save_sent_messages(msg_ids):
    with open(SENT_MESSAGES_FILE, "w") as f:
        json.dump(msg_ids, f)

def load_sent_messages():
    if os.path.exists(SENT_MESSAGES_FILE):
        with open(SENT_MESSAGES_FILE, "r") as f:
            return json.load(f)
    return []

def add_sent_message(msg_id):
    msgs = load_sent_messages()
    if msg_id not in msgs:
        msgs.append(msg_id)
    save_sent_messages(msgs)

def clear_sent_messages():
    if os.path.exists(SENT_MESSAGES_FILE):
        os.remove(SENT_MESSAGES_FILE)


PURPLE_GRADIENT = [
    Fore.MAGENTA + Style.BRIGHT,
    Fore.MAGENTA,
    Fore.MAGENTA + Style.DIM,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTMAGENTA_EX + Style.BRIGHT
]

BANNER_LINES = [
"           ________   ___  ___   ________   ________    _________   ________   _____ ______       ___    ___ ",
"          |\\   __  \\ |\\  \\|\\  \\ |\\   __  \\ |\\   ___  \\ |\\___   ___\\|\\   __  \\ |\\   _ \\  _   \\    |\\  \\  /  /|",
"          \\ \\  \\|\\  \\\\ \\  \\\\\\  \\\\ \\  \\|\\  \\\\ \\  \\\\ \\  \\\\|___ \\  \\_|\\ \\  \\|\\  \\\\ \\  \\\\\\__\\ \\  \\   \\ \\  \\/  / /",
"           \\ \\   ____\\\\ \\   __  \\\\ \\   __  \\\\ \\  \\\\ \\  \\    \\ \\  \\  \\ \\  \\\\\\  \\\\ \\  \\\\|__| \\  \\   \\ \\    / / ",
"            \\ \\  \\___| \\ \\  \\ \\  \\\\ \\  \\ \\  \\\\ \\  \\\\ \\  \\    \\ \\  \\  \\ \\  \\\\\\  \\\\ \\  \\    \\ \\  \\   /     \\/  ",
"             \\ \\__\\     \\ \\__\\ \\__\\\\ \\__\\ \\__\\\\ \\__\\\\ \\__\\    \\ \\__\\  \\ \\_______\\\\ \\__\\    \\ \\__\\ /  /\\   \\  ",
"              \\|__|      \\|__|\\|__| \\|__|\\|__| \\|__| \\|__|     \\|__|   \\|_______| \\|__|     \\|__|/__/ /\\ __\\ "
]

def print_banner():
    width = 80
    for i, line in enumerate(BANNER_LINES):
        color = PURPLE_GRADIENT[i % len(PURPLE_GRADIENT)]
        print(color + line.center(width) + Style.RESET_ALL)

def print_menu(logged_in):
    print()
    if not logged_in:
        print(f"{Fore.LIGHTMAGENTA_EX}1.{Style.RESET_ALL} Login with Webhook URL")
        print(f"{Fore.LIGHTMAGENTA_EX}2.{Style.RESET_ALL} Logout")
        print(f"{Fore.LIGHTMAGENTA_EX}0.{Style.RESET_ALL} Exit")
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}1.{Style.RESET_ALL} Get Webhook Info")
        print(f"{Fore.LIGHTMAGENTA_EX}2.{Style.RESET_ALL} Send Message")
        print(f"{Fore.LIGHTMAGENTA_EX}3.{Style.RESET_ALL} Send Embed")
        print(f"{Fore.LIGHTMAGENTA_EX}4.{Style.RESET_ALL} Edit Message")
        print(f"{Fore.LIGHTMAGENTA_EX}5.{Style.RESET_ALL} Delete Message")
        print(f"{Fore.LIGHTMAGENTA_EX}6.{Style.RESET_ALL} Spam Messages")
        print(f"{Fore.LIGHTMAGENTA_EX}7.{Style.RESET_ALL} Delete Webhook")
        print(f"{Fore.LIGHTMAGENTA_EX}8.{Style.RESET_ALL} Delete All Sent Messages")
        print(f"{Fore.LIGHTMAGENTA_EX}9.{Style.RESET_ALL} Logout")
        print(f"{Fore.LIGHTMAGENTA_EX}0.{Style.RESET_ALL} Exit")


def validate_webhook(url):
    try:
        r = requests.get(url)
        return r.status_code == 200
    except:
        return False

def get_webhook_info(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            info = r.json()
            print(f"Name: {info.get('name')}")
            print(f"ID: {info.get('id')}")
            print(f"Channel ID: {info.get('channel_id')}")
            print(f"Guild ID: {info.get('guild_id')}")
        else:
            print("Failed to fetch webhook info.")
    except Exception as e:
        print(f"Error: {e}")

def send_message(url, content, username=None, avatar_url=None, tts=False):
    data = {
        "content": content,
        "tts": tts
    }
    if username:
        data["username"] = username
    if avatar_url:
        data["avatar_url"] = avatar_url

    try:
        r = requests.post(url, json=data)
        if r.status_code in (200, 204):
            print("Message sent!")
            if r.status_code == 200:
                msg_id = r.json().get("id")
                if msg_id:
                    add_sent_message(msg_id)
        else:
            print(f"Failed to send message. Status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def create_embed():
    title = input("Embed title: ")
    description = input("Embed description: ")
    color_input = input("Embed color (hex without #, e.g. 7289DA): ")
    try:
        color = int(color_input, 16)
    except:
        color = 0x7289DA
    embed = {
        "title": title,
        "description": description,
        "color": color
    }
    return embed

def send_embed(url, embed, username=None, avatar_url=None, tts=False):
    data = {
        "embeds": [embed],
        "tts": tts
    }
    if username:
        data["username"] = username
    if avatar_url:
        data["avatar_url"] = avatar_url
    try:
        r = requests.post(url, json=data)
        if r.status_code in (200, 204):
            print("Embed sent!")
            if r.status_code == 200:
                msg_id = r.json().get("id")
                if msg_id:
                    add_sent_message(msg_id)
        else:
            print(f"Failed to send embed. Status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def edit_message(url, message_id, new_content=None, new_embed=None, username=None, avatar_url=None):
    data = {}
    if new_content is not None:
        data["content"] = new_content
    if new_embed is not None:
        data["embeds"] = [new_embed]
    if username:
        data["username"] = username
    if avatar_url:
        data["avatar_url"] = avatar_url
    if not data:
        print("Nothing to update.")
        return
    try:
        r = requests.patch(f"{url}/messages/{message_id}", json=data)
        if r.status_code == 200:
            print("Message edited successfully.")
        else:
            print(f"Failed to edit message. Status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def delete_message(url, message_id):
    try:
        r = requests.delete(f"{url}/messages/{message_id}")
        if r.status_code == 204:
            print("Message deleted successfully.")
            msgs = load_sent_messages()
            if message_id in msgs:
                msgs.remove(message_id)
                save_sent_messages(msgs)
        else:
            print(f"Failed to delete message. Status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def spam_messages(url, content, count, delay, username=None, avatar_url=None, tts=False):
    for i in range(count):
        send_message(url, content, username, avatar_url, tts)
        time.sleep(delay)

def delete_webhook(url):
    try:
        r = requests.delete(url)
        if r.status_code == 204:
            print("Webhook deleted successfully.")
            clear_session()
            clear_sent_messages()
            return True
        else:
            print(f"Failed to delete webhook. Status code: {r.status_code}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def delete_all_sent_messages(url):
    msgs = load_sent_messages()
    if not msgs:
        print("No sent messages recorded.")
        return
    print(f"Attempting to delete {len(msgs)} messages sent by this webhook...")
    success = 0
    for msg_id in msgs[:]:
        try:
            r = requests.delete(f"{url}/messages/{msg_id}")
            if r.status_code == 204:
                success += 1
                msgs.remove(msg_id)
                save_sent_messages(msgs)
                print(f"Deleted message {msg_id}")
            else:
                print(f"Failed to delete message {msg_id} (Status: {r.status_code})")
        except Exception as e:
            print(f"Error deleting message {msg_id}: {e}")
    print(f"Deleted {success} messages successfully.")


def main():
    session = load_session()
    webhook_url = session.get("webhook_url")
    logged_in = bool(webhook_url)

    while True:
        clear_screen()
        print_banner()
        print_menu(logged_in)
        print()
        if logged_in:
            print()
            print(f"{Fore.LIGHTMAGENTA_EX}Current webhook:{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}{webhook_url}{Style.RESET_ALL}")
            print()

        choice = input("Choose an option: ").strip()

        if not logged_in:
            if choice == "1":
                url = input("Enter webhook URL: ").strip()
                print("Validating webhook...")
                if validate_webhook(url):
                    webhook_url = url
                    save_session({"webhook_url": webhook_url})
                    logged_in = True
                    print("Logged in and session saved.")
                else:
                    print("Invalid webhook URL or cannot connect.")
                input("Press Enter to continue...")

            elif choice == "2":
                print("You are not logged in.")
                input("Press Enter to continue...")

            elif choice == "0":
                print("Goodbye!")
                time.sleep(1)
                sys.exit(0)

            else:
                print("Invalid choice.")
                time.sleep(1.5)

        else:
            if choice == "1":
                clear_screen()
                get_webhook_info(webhook_url)
                input("\nPress Enter to return to menu...")

            elif choice == "2":
                content = input("Message content: ")
                username = input("Override username (leave blank to skip): ").strip() or None
                avatar_url = input("Override avatar URL (leave blank to skip): ").strip() or None
                tts = input("Use TTS? (y/n): ").lower() == "y"
                send_message(webhook_url, content, username, avatar_url, tts)
                input("\nPress Enter to continue...")

            elif choice == "3":
                embed = create_embed()
                username = input("Override username (leave blank to skip): ").strip() or None
                avatar_url = input("Override avatar URL (leave blank to skip): ").strip() or None
                tts = input("Use TTS? (y/n): ").lower() == "y"
                send_embed(webhook_url, embed, username, avatar_url, tts)
                input("\nPress Enter to continue...")

            elif choice == "4":
                message_id = input("Message ID to edit: ").strip()
                new_content = input("New content (leave blank to skip): ")
                new_embed = None
                use_embed = input("Edit embed? (y/n): ").lower() == "y"
                if use_embed:
                    new_embed = create_embed()
                username = input("Override username (leave blank to skip): ").strip() or None
                avatar_url = input("Override avatar URL (leave blank to skip): ").strip() or None
                edit_message(webhook_url, message_id, new_content or None, new_embed, username, avatar_url)
                input("\nPress Enter to continue...")

            elif choice == "5":
                message_id = input("Message ID to delete: ").strip()
                confirm = input(f"Delete message {message_id}? (yes/no): ").lower()
                if confirm == "yes":
                    delete_message(webhook_url, message_id)
                else:
                    print("Deletion cancelled.")
                input("\nPress Enter to continue...")

            elif choice == "6":
                content = input("Message content to spam: ")
                count = input("Number of messages to send: ")
                delay = input("Delay between messages (seconds): ")
                username = input("Override username (leave blank to skip): ").strip() or None
                avatar_url = input("Override avatar URL (leave blank to skip): ").strip() or None
                tts = input("Use TTS? (y/n): ").lower() == "y"
                try:
                    count = int(count)
                    delay = float(delay)
                    spam_messages(webhook_url, content, count, delay, username, avatar_url, tts)
                except Exception as e:
                    print(f"Invalid input: {e}")
                input("\nPress Enter to continue...")

            elif choice == "7":
                confirm = input("Delete webhook permanently? (yes/no): ").lower()
                if confirm == "yes":
                    if delete_webhook(webhook_url):
                        webhook_url = None
                        logged_in = False
                else:
                    print("Deletion cancelled.")
                input("\nPress Enter to continue...")

            elif choice == "8":
                confirm = input("Delete ALL sent messages? (yes/no): ").lower()
                if confirm == "yes":
                    delete_all_sent_messages(webhook_url)
                else:
                    print("Cancelled.")
                input("\nPress Enter to continue...")

            elif choice == "9":
                clear_session()
                clear_sent_messages()
                webhook_url = None
                logged_in = False
                print("Logged out.")
                input("\nPress Enter to continue...")

            elif choice == "0":
                print("Goodbye!")
                time.sleep(1)
                sys.exit(0)

            else:
                print("Invalid choice.")
                time.sleep(1.5)

if __name__ == "__main__":
    main()