from datetime import date


def prepare_text(text, target, img):
    if target is 'site':
        return prepare_text_for_site(text,img)
    elif target is 'twi':
        return get_first_sentence
    elif target is 'inst':
        return get_first_sentence()
    return


def remove_tag(text):
    return text.replace('@samara_it_community', '')


def prepare_text_for_site(text, img):
    result = '+++\n title = "' + get_first_sentence(text) + '\n" date = ' + date.today().strftime(
        "%Y-%m-%d") + '\ndescription = ""'
    result += '\n+++'
    result += '\n<!-- more -->\n'
    result += text + '\n'
    for i in range(len(img)):
        result += '\n![]('+img[i]+'/700x700)'
    return result


def find_pos_of_first_separator(text):
    return min(text.find('.'), text.find('!'), text.find('?'))


def get_first_sentence(text):
    return text[0:find_pos_of_first_separator(text)]
