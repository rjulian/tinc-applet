import configparser
import os

CONFIG_FILE_PATH = os.path.expanduser("~/.tincapplet")

# Default values
check_interval = 300
show_notifications = True


def __load():
    if not os.path.isfile(CONFIG_FILE_PATH):
        persist()
        return
    global check_interval
    global show_notifications
    global check_for_updates
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    check_interval = int(config['DEFAULT']['CheckInterval'])
    show_notifications = config['DEFAULT'].getboolean('ShowNotifications')



def persist():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'CheckInterval':check_interval,
                         'ShowNotifications':show_notifications}
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

__load()
