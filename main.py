from api_methods import *
import time


def main():
    last_textchat = (None, None)
    while True:
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text, chat) != last_textchat:
            send_message(text, chat)
            last_textchat = (text, chat)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
