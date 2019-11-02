from datetime import date
import math

SITE = 'site'
TWITTER = 'twitter'
INSTAGRAM = 'instagram'


def prepare_text(text, target, img):
    if target is SITE:
        return prepare_text_for_site(text, img)
    elif target is TWITTER:
        return get_first_sentence(text)
    elif target is INSTAGRAM:
        return get_first_sentence(text)
    return


def remove_tag(text):
    return text.replace('@samara_it_community', '')


def prepare_text_for_site(text, img):
    result = '+++\n title = "' + get_first_sentence(text) + '" \n date = ' + date.today().strftime(
        "%Y-%m-%d") + '\ndescription = "test"'
    result += '\n+++'
    result += '\n<!-- more -->\n'
    result += text + '\n'
    for i in range(len(img)):
        result += '\n![]('+img[i]+')'
    return result


def find_pos_of_first_separator(text):
    dot = text.find('.')
    vosk = text.find('!')
    vop = text.find('?')
    dot=math.inf if dot == -1 else dot
    vosk = math.inf if vosk == -1 else vosk
    vop = math.inf if vop == -1 else vop
    return min(dot, vosk, vop)


def get_first_sentence(text):
    return text[0:find_pos_of_first_separator(text)]


# if __name__ == '__main__':
#     print(prepare_text_for_site(long_string,[]))