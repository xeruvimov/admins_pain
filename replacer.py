from datetime import date
import math

SITE = 'site'
TWITTER = 'twitter'
INSTAGRAM = 'instagram'
TELEGRAM = 'tlg'


def prepare_text(text, target, img):
    res_text = remove_tag(text)
    res_text = replace_tag_with_link(res_text)
    if target is SITE:
        return prepare_text_for_site(res_text, img)
    elif target is TWITTER:
        return get_first_sentence(res_text)
    elif target is INSTAGRAM:
        return get_first_sentence(res_text)
    elif target is TELEGRAM:
        return res_text
    return


def replace_tag_with_link(text):
    if '@' in text:
        return text.replace('@', 'vk.com/')


def remove_tag(text):
    return text.replace('@samara_it_community', '')


def prepare_text_for_site(text, img):
    result = '+++\n title = "' + get_first_sentence(text) + '" \n date = ' + date.today().strftime(
        "%Y-%m-%d") + '\ndescription = "test"'
    result += '\n+++'
    result += '\n<!-- more -->\n'
    result += text + '\n'
    if img is not None:
        for i in img:
            result += '\n![](' + img[i] + ')'
    return result


# def find_pos_of_first_separator(text):
#     return text.find('\n')
    # dot = text.find('.')
    # vosk = text.find('!')
    # vop = text.find('?')
    # dot=math.inf if dot == -1 else dot
    # vosk = math.inf if vosk == -1 else vosk
    # vop = math.inf if vop == -1 else vop
    # return min(dot, vosk, vop)


def get_first_sentence(text):
    return text.split('\n')[0]
    # return text[0:find_pos_of_first_separator(text)]


# if __name__ == '__main__':
#     print(prepare_text_for_site(long_string,[]))