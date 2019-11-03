import threading
import traceback
from datetime import date
from datetime import datetime
import telebot
import vk_api
from telebot.types import InputMediaPhoto
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import data
import replacer

start_msg = "Start listen just now"
message_breakers = [':', ' ', '\n']
max_message_length = 4091

bot = telebot.TeleBot(data.BOT_TOKEN)
vk_session = None
vk_long_poll = None

repost_image_urls = None
original_post_img_urls = None


def get_session():
    global vk_session

    if vk_session is None:
        vk_session = vk_api.VkApi(token=data.GROUP_TOKEN)
        return vk_session
    else:
        return vk_session


def get_longpoll():
    global vk_long_poll

    if vk_long_poll is None:
        vk_long_poll = VkBotLongPoll(get_session(), data.GROUP_ID, 60)
        return vk_long_poll
    else:
        return vk_long_poll


def check_posts_vk(chat_id):
    global bot
    global original_post_img_urls

    longpoll = get_longpoll()

    print(start_msg)
    bot.send_message(data.MY_CHAT_ID, start_msg)

    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            post = event.obj
            print('------------------------------------------------------------------------------------------------')
            print(post)

            text = post['text']

            images = []
            links = []
            doc = []
            attachments = []
            if 'attachments' in post:
                attach = post['attachments']
                for add in attach:
                    if add['type'] == 'photo':
                        img = add['photo']
                        images.append(img)
                    elif add['type'] == 'video':
                        video = add['video']
                        if 'player' in video:
                            links.append(video['player'])
                    elif add['type'] == 'doc':
                        docs = add['doc']
                        if 'url' in docs:
                            doc.append(docs['title'])
                            doc.append(docs['url'])
                    else:
                        for (key, value) in add.items():
                            if key != 'type' and 'url' in value:
                                attachments.append(value['url'])

            print(doc, '\n')

            if len(doc) != 0:
                text += '\n'
                text += '\n'.join(doc)
            send_posts_text(text, chat_id)

            if len(images) > 0:
                original_post_img_urls = list(
                    map(lambda img: max(img["sizes"], key=lambda size: size["type"])["url"], images))
                print(original_post_img_urls)
                bot.send_media_group(chat_id, map(lambda url: InputMediaPhoto(url), original_post_img_urls))

            bot.send_message(data.MY_CHAT_ID, "News posted on telegram")
            create_site_post(text)
            bot.send_message(data.MY_CHAT_ID, "News posted on site")
            # if 'copy_history' in post:
            #     copy_history = post['copy_history']
            #     copy_history = copy_history[0]
            #     print('--copy_history--')
            #     print(copy_history)
            #     text = copy_history['text']
            #     send_posts_text(text, chat_id)
            #
            #     if 'attachments' in copy_history:
            #         copy_add = copy_history['attachments']
            #         copy_add = copy_add[0]
            #
            #         if copy_add['type'] == 'link':
            #             link = copy_add['link']
            #             text = link['title']
            #             send_posts_text(text, chat_id)
            #             img = link['photo']
            #             send_posts_img(img, chat_id)
            #             url = link['url']
            #             send_posts_text(url, chat_id)
            #
            #         if copy_add['type'] == 'photo':
            #             attach = copy_history['attachments']
            #             for img in attach:
            #                 image = img['photo']
            #                 send_posts_img(image, chat_id)
            #
            #         if copy_add['type'] == 'doc':
            #             attach = copy_history['attachments']
            #             for doc in attach:
            #                 text = doc['doc']['title'] + '\n' + doc['doc']['url']
            #                 send_posts_text(text, chat_id)


def create_site_post(text):
    site_text = replacer.prepare_text(text, 'site', original_post_img_urls)
    print(site_text)
    file_path = data.PATH_TO_SITE_PAGES + str(date.today().strftime("%Y-%m-%d")) + str(datetime.now().hour) + str(
        datetime.now().minute) + str(datetime.now().second) + ".md"
    print(file_path)
    page_file = open(file_path, 'w+', encoding='utf-8')
    page_file.write(site_text)
    page_file.close()


def send_posts_text(text, chat_id):
    global bot

    if text == '':
        print('no text')
    else:
        for msg in split(text):
            bot.send_message(chat_id, msg)


def split(text):
    global message_breakers
    global max_message_length

    if len(text) >= max_message_length:
        last_index = max(
            map(lambda separator: text.rfind(separator, 0, max_message_length), message_breakers))
        good_part = text[:last_index]
        bad_part = text[last_index + 1:]
        return [good_part] + split(bad_part)
    else:
        return [text]


# def send_posts_img(img, chat_id):
#     global bot
#     global repost_image_urls
#
#     repost_image_urls = list(map(lambda img: max(img["sizes"], key=lambda size: size["type"])["url"], img))
#     print(repost_image_urls)
#     bot.send_media_group(chat_id, map(lambda url: InputMediaPhoto(url), repost_image_urls))
#
#     print(img['sizes'][-1])


@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, "I`m still work")


if __name__ == '__main__':
    bot_polling_thread = threading.Thread(target=bot.polling, args=())
    bot_polling_thread.start()

    try:
        check_posts_vk(data.CHANEL_ID)
    except Exception:
        bot.send_message(data.MY_CHAT_ID, traceback.format_exc())
        bot.send_message(data.MY_CHAT_ID, "Stop check new posts")
        bot.send_message(data.MY_CHAT_ID, "Attempt to restore work")
        try:
            check_posts_vk(data.CHANEL_ID)
        except Exception:
            bot.send_message(data.MY_CHAT_ID, traceback.format_exc())
            bot.send_message(data.MY_CHAT_ID, "Stop check new posts\nRestart me")
