import os
from logger import log


class Config:
    def __init__(self):
        self.max_messages = 1000
        self.extensions_document = [".docx", ".txt"]
        self.screen_unread_messages = False
        self.screen_group = False
        self.screen_contact = False
        self.screen_channel = False
        self.screen_bot = False
        self.firefox_profile = os.environ["MProfile"]
        self.download_folder = "C:\\Download"

    def parse_config(self, name_config_file):
        try:
            with open(name_config_file, "r") as file:
                for line in file:
                    line = line.strip()
                    index_comment = line.find('#')
                    if index_comment != -1:
                        line = line[:index_comment]
                    index_separator = line.find(':')

                    if index_separator == -1 or (index_separator + 1) == len(line):
                        continue

                    key = line[:index_separator]
                    value = line[(index_separator + 1):].split()

                    if key.strip() == "MAX_MESSAGES":
                        if len(value) == 1:
                            self.max_messages = int(value[0].strip())
                    elif key.strip() == "FIREFOX_PROFILE":
                        if len(value) == 1:
                            self.firefox_profile = value[0]
                    elif key.strip() == "SCREEN_UNREAD_MESSAGES":
                        if len(value) == 1:
                            if value[0].strip() == "False":
                                self.screen_unread_messages = False
                            elif value[0].strip() == "True":
                                self.screen_unread_messages = True
                    elif key.strip() == "SCREEN_GROUP":
                        if len(value) == 1:
                            if value[0].strip() == "False":
                                self.screen_group = False
                            elif value[0].strip() == "True":
                                self.screen_group = True
                    elif key.strip() == "SCREEN_CONTACT":
                        if len(value) == 1:
                            if value[0].strip() == "False":
                                self.screen_contact = False
                            elif value[0].strip() == "True":
                                self.screen_contact = True
                    elif key.strip() == "SCREEN_CHANNEL":
                        if len(value) == 1:
                            if value[0].strip() == "False":
                                self.screen_channel = False
                            elif value[0].strip() == "True":
                                self.screen_channel = True
                    elif key.strip() == "SCREEN_BOT":
                        if len(value) == 1:
                            if value[0].strip() == "False":
                                self.screen_bot = False
                            elif value[0].strip() == "True":
                                self.screen_bot = True
                    elif key.strip() == "EXTENSIONS_DOCUMENT":
                        self.extensions_document.clear()
                        for v in value:
                            self.extensions_document.append(v.strip())
                    elif key.strip() == "DOWNLOAD_FOLDER":
                        if len(value) == 1:
                            self.download_folder = value[0]
        except FileNotFoundError:
            log.info(
                "Конфиг файл config.txt не найден. Применены настройки по умолчанию")
        except Exception:
            log.info("Произошла ошибка в разборе конфиг файла config.txt")
