from dbhelper import DBHelper
from api_methods import *
import time

db = DBHelper()


def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            items = db.get_items(chat)

            if text == '/done':
                keyboard = build_keyboard(items)
                send_message("Select an item to delete", chat, keyboard)
            elif text == "/start":
                send_message(
                    "Welcome to your personal To Do list. Send any text to me and I'll store it as an item. "
                    "Send /done to remove items",
                    chat)
            elif text.startswith("/"):
                continue
            elif text in items:
                db.delete_item(text, chat)
                items = db.get_items(chat)
                keyboard = build_keyboard(items)
                send_message("Select an item to delete", chat, keyboard)
            else:
                db.add_item(text, chat)
                items = db.get_items(chat)
                message = "\n".join(items)
                send_message(message, chat)

        except KeyError:
            pass


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
