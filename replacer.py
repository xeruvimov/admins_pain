from datetime import date

def remove_tag(text):
    return text.replace('@samara_it_community', '')


def prepare_text(text):
    result = '+++\n title = "' + getFirstSentence(text) + '\n" date = ' + date.today().strftime(
        "%Y-%m-%d") + '\ndescription = ""'
    result += '\n+++'
    result += '\n<!-- more -->'
    result += text
    print(result)


def findPosOfFirstSeparator(text):
    return min(text.find('.'), text.find('!'), text.find('?'))


def getFirstSentence(text):
    return text[0:findPosOfFirstSeparator(text)]
