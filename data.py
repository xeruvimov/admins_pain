import configparser

config_path = 'settings.ini'
config = configparser.ConfigParser()
config.read(config_path)
GROUP_TOKEN = config.get('VK', 'GROUP_TOKEN')
GROUP_ID = config.get('VK', 'GROUP_ID')
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
MY_CHAT_ID = config.get('Telegram', 'MY_CHAT_ID')
CHANEL_ID = config.get('Telegram', 'CHANEL_ID')
