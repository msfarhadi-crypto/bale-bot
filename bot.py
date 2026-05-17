import requests
import time
import json
import os

TOKEN = "354006773:CucJArJPcYD-Q4HvvZQofjaPChe2ZocHP6s"
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

last_update_id = 0
user_quiz_state = {}

SCORES_FILE = "scores.json"

# ---------- خواندن امتیازها ----------
def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {}

# ---------- ذخیره امتیاز ----------
def save_scores(scores):
    with open(SCORES_FILE,"w",encoding="utf-8") as f:
        json.dump(scores,f)

user_scores = load_scores()

# ---------- منوی اصلی ----------
def main_menu():
    return {
        "keyboard":[
            [{"text":"📚 شروع دوره پایتون"}],
            [{"text":"🏆 امتیاز من"}],
            [{"text":"🥇 رتبه بندی"}],
            [{"text":"🤖 درباره ربات"}]
        ],
        "resize_keyboard":True
    }

# ---------- منوی درس ----------
def lessons_menu():
    return {
        "keyboard":[
            [{"text":"درس ۱: پایتون چیست؟"}],
            [{"text":"درس ۲: نصب پایتون"}],
            [{"text":"درس ۳: دستور Print"}],
            [{"text":"درس ۴: متغیرها"}],
            [{"text":"🔙 بازگشت به منوی اصلی"}]
        ],
        "resize_keyboard":True
    }

# ---------- دکمه آزمون ----------
def quiz_buttons():
    return {
        "keyboard":[
            [{"text":"الف) فقط برای هوش مصنوعی"}],
            [{"text":"ب) برای ساخت سایت و هوش مصنوعی"}],
            [{"text":"ج) فقط برای بازی سازی"}],
            [{"text":"د) فقط برای موبایل"}],
            [{"text":"❌ انصراف"}]
        ],
        "resize_keyboard":True
    }

# ---------- ارسال پیام ----------
def send_message(chat_id,text,keyboard=None):

    url = f"{BASE_URL}/sendMessage"

    data = {
        "chat_id":chat_id,
        "text":text
    }

    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)

    requests.post(url,json=data)

# ---------- رتبه بندی ----------
def leaderboard():

    if not user_scores:
        return "هنوز کسی امتیاز نگرفته."

    sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

    text = "🏆 رتبه بندی کاربران\n\n"

    rank = 1
    for user,score in sorted_users[:10]:
        text += f"{rank}️⃣ کاربر {user} — {score} امتیاز\n"
        rank += 1

    return text

# ---------- مدیریت پیام ----------
def handle_message(chat_id,text):

    # start
    if text == "/start":
        send_message(chat_id,"سلام 👋 به ربات آموزش پایتون خوش آمدی",main_menu())

    # شروع دوره
    elif text == "📚 شروع دوره پایتون":
        send_message(chat_id,"یکی از درس‌ها را انتخاب کن",lessons_menu())

    # امتیاز
    elif text == "🏆 امتیاز من":
        score = user_scores.get(str(chat_id),0)
        send_message(chat_id,f"🏆 امتیاز شما: {score}",main_menu())

    # رتبه بندی
    elif text == "🥇 رتبه بندی":
        send_message(chat_id,leaderboard(),main_menu())

    # درباره
    elif text == "🤖 درباره ربات":
        send_message(chat_id,"این ربات برای آموزش پایتون ساخته شده 🚀",main_menu())

    # ---------- درس 1 ----------
    elif text == "درس ۱: پایتون چیست؟":

        msg = """
📘 درس ۱: پایتون چیست؟

پایتون یک زبان برنامه نویسی ساده و قدرتمند است.

کاربردها:
✅ هوش مصنوعی
✅ ساخت سایت
✅ تحلیل داده
"""

        keyboard = {
            "keyboard":[
                [{"text":"شروع آزمون درس ۱"}],
                [{"text":"➡️ درس بعدی"}],
                [{"text":"🔙 بازگشت به منوی اصلی"}]
            ],
            "resize_keyboard":True
        }

        send_message(chat_id,msg,keyboard)

    # ---------- درس 2 ----------
    elif text == "درس ۲: نصب پایتون" or text == "➡️ درس بعدی":

        msg = """
📘 درس ۲: نصب پایتون

1️⃣ برو به سایت python.org
2️⃣ نسخه ویندوز را دانلود کن
3️⃣ موقع نصب گزینه Add Python to PATH را فعال کن
"""

        keyboard = {
            "keyboard":[
                [{"text":"درس ۳: دستور Print"}],
                [{"text":"🔙 بازگشت به منوی اصلی"}]
            ],
            "resize_keyboard":True
        }

        send_message(chat_id,msg,keyboard)

    # ---------- درس 3 ----------
    elif text == "درس ۳: دستور Print":

        msg = """
📘 درس ۳: دستور print

مثال:

print("Hello World")

این دستور متن را در خروجی نشان می‌دهد.
"""

        keyboard = {
            "keyboard":[
                [{"text":"درس ۴: متغیرها"}],
                [{"text":"🔙 بازگشت به منوی اصلی"}]
            ],
            "resize_keyboard":True
        }

        send_message(chat_id,msg,keyboard)

    # ---------- درس 4 ----------
    elif text == "درس ۴: متغیرها":

        msg = """
📘 درس ۴: متغیرها

مثال:

name = "Ali"
age = 20
"""

        send_message(chat_id,msg,lessons_menu())

    # ---------- شروع آزمون ----------
    elif text == "شروع آزمون درس ۱":

        user_quiz_state[chat_id] = True

        send_message(
            chat_id,
            "سوال:\nپایتون بیشتر در چه زمینه‌ای استفاده می‌شود؟",
            quiz_buttons()
        )

    # ---------- پاسخ آزمون ----------
    elif chat_id in user_quiz_state:

        if text == "ب) برای ساخت سایت و هوش مصنوعی":

            uid = str(chat_id)

            user_scores[uid] = user_scores.get(uid,0) + 10

            save_scores(user_scores)

            send_message(
                chat_id,
                f"✅ پاسخ درست!\n🏆 امتیاز شما: {user_scores[uid]}",
                lessons_menu()
            )

        elif text == "❌ انصراف":

            send_message(chat_id,"آزمون لغو شد",lessons_menu())

        else:

            send_message(chat_id,"❌ پاسخ اشتباه بود",lessons_menu())

        del user_quiz_state[chat_id]

    elif text == "🔙 بازگشت به منوی اصلی":
        send_message(chat_id,"منوی اصلی",main_menu())

# ---------- حلقه اصلی ----------
print("✅ ربات اجرا شد")

while True:

    url = f"{BASE_URL}/getUpdates?offset={last_update_id}"

    try:

        res = requests.get(url).json()

        for update in res["result"]:

            last_update_id = update["update_id"] + 1

            if "message" in update:

                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text","")

                handle_message(chat_id,text)

    except:
        print("خطای اتصال")

    time.sleep(1)
