'''
:copyright: (c) 2020 by lavrovsergei97
:license: Apache2, see LICENSE for more details.
'''

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
        self.firefox_profile = ""
        self.download_folder = ""
        self.geckodriver = ""

    def print_parametrs(self):
        log.info(f"""Параметры профиля: 
                     MAX_MESSAGES: {self.max_messages}
                     GECKODRIVER: {self.geckodriver}
                     FIREFOX_PROFILE: {self.firefox_profile}
                     SCREEN_UNREAD_MESSAGES: {self.screen_unread_messages}
                     SCREEN_GROUP: {self.screen_group}
                     SCREEN_CONTACT: {self.screen_contact}
                     SCREEN_CHANNEL: {self.screen_channel}
                     SCREEN_BOT: {self.screen_bot}
                     EXTENSIONS_DOCUMENT: {self.extensions_document}
                     DOWNLOAD_FOLDER: {self.download_folder}""")

    def parse_config(self, name_config_file):
        try:
            with open(name_config_file, "r", encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    index_comment = line.find('#')
                    if index_comment != -1:
                        line = line[:index_comment]
                    index_separator = line.find(':')

                    if index_separator == -1 or (index_separator + 1) == len(line):
                        continue

                    key = line[:index_separator]
                    value = line[(index_separator + 1):]

                    if key.strip() == "MAX_MESSAGES":
                        parametrs = value.split()
                        if len(parametrs) == 1:
                            self.max_messages = int(parametrs[0].strip())
                        else:
                            log.info("Неверный формат параметра MAX_MESSAGES")
                    elif key.strip() == "GECKODRIVER":
                        self.geckodriver = value.strip()
                    elif key.strip() == "FIREFOX_PROFILE":
                        self.firefox_profile = value.strip()
                    elif key.strip() == "SCREEN_UNREAD_MESSAGES":
                        parametrs = value.split()
                        if len(parametrs) == 1:
                            if parametrs[0].strip() == "False":
                                self.screen_unread_messages = False
                            elif parametrs[0].strip() == "True":
                                self.screen_unread_messages = True
                            else:
                                log.info(
                                    "Неверный формат параметра SCREEN_UNREAD_MESSAGES. Допустимые значения: False, True")
                        else:
                            log.info(
                                "Неверный формат параметра SCREEN_UNREAD_MESSAGES")
                    elif key.strip() == "SCREEN_GROUP":
                        parametrs = value.split()
                        if len(parametrs) == 1:
                            if parametrs[0].strip() == "False":
                                self.screen_group = False
                            elif parametrs[0].strip() == "True":
                                self.screen_group = True
                            else:
                                log.info(
                                    "Неверный формат параметра SCREEN_GROUP. Допустимые значения: False, True")
                        else:
                            log.info(
                                "Неверный формат параметра SCREEN_GROUP")
                    elif key.strip() == "SCREEN_CONTACT":
                        parametrs = value.split()
                        if len(parametrs) == 1:
                            if parametrs[0].strip() == "False":
                                self.screen_contact = False
                            elif parametrs[0].strip() == "True":
                                self.screen_contact = True
                            else:
                                log.info(
                                    "Неверный формат параметра SCREEN_CONTACT. Допустимые значения: False, True")
                        else:
                            log.info(
                                "Неверный формат параметра SCREEN_CONTACT")
                    elif key.strip() == "SCREEN_CHANNEL":
                        parametrs = value.split()
                        if len(parametrs) == 1:
                            if parametrs[0].strip() == "False":
                                self.screen_channel = False
                            elif parametrs[0].strip() == "True":
                                self.screen_channel = True
                            else:
                                log.info(
                                    "Неверный формат параметра SCREEN_CHANNEL. Допустимые значения: False, True")
                        else:
                            log.info(
                                "Неверный формат параметра SCREEN_CHANNEL")
                    elif key.strip() == "SCREEN_BOT":
                        parametrs = value.split()
                        if len(parametrs) == 1:
                            if parametrs[0].strip() == "False":
                                self.screen_bot = False
                            elif parametrs[0].strip() == "True":
                                self.screen_bot = True
                            else:
                                log.info(
                                    "Неверный формат параметра SCREEN_BOT. Допустимые значения: False, True")
                        else:
                            log.info(
                                "Неверный формат параметра SCREEN_BOT")
                    elif key.strip() == "EXTENSIONS_DOCUMENT":
                        parametrs = value.split()
                        self.extensions_document.clear()
                        for p in parametrs:
                            self.extensions_document.append(p.strip())
                    elif key.strip() == "DOWNLOAD_FOLDER":
                        self.download_folder = value.strip()
        except FileNotFoundError:
            log.info(
                "Конфиг файл config.txt не найден. Применены настройки по умолчанию")
        except Exception:
            log.info("Произошла ошибка в разборе конфиг файла config.txt")
