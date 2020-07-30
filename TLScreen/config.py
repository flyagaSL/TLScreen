import os


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
        self.download_folder = ".\\"

    def parse_config(self, name_config_file):
        with open(name_config_file, "r") as file:
            for line in file:
                line = line.strip()
                index_comment = line.find('#')
                if index_comment != -1:
                    line = line[:index_comment]
                parametrs = line.split(':')
                if len(parametrs) == 1:
                    continue
                values = parametrs[1].split()
                if parametrs[0].strip() == "MAX_MESSAGES":
                    if len(values) == 1:
                        self.max_messages = int(values[0].strip())
                elif parametrs[0].strip() == "FIREFOX_PROFILE":
                    if len(values) == 1:
                        self.firefox_profile = values[0]
                elif parametrs[0].strip() == "DOWNLOAD_FOLDER":
                    if len(values) == 1:
                        self.download_folder = values[0]
                elif parametrs[0].strip() == "SCREEN_UNREAD_MESSAGES":
                    if len(values) == 1:
                        self.screen_unread_messages = bool(values[0].strip())
                elif parametrs[0].strip() == "SCREEN_GROUP":
                    if len(values) == 1:
                        self.screen_group = bool(values[0].strip())
                elif parametrs[0].strip() == "SCREEN_CONTACT":
                    if len(values) == 1:
                        self.screen_contact = bool(values[0].strip())
                elif parametrs[0].strip() == "SCREEN_CHANNEL":
                    if len(values) == 1:
                        self.screen_channel = bool(values[0].strip())
                elif parametrs[0].strip() == "SCREEN_BOT":
                    if len(values) == 1:
                        self.screen_bot = bool(values[0].strip())
                elif parametrs[0].strip() == "EXTENSIONS_DOCUMENT":
                    self.extensions_document.clear()
                    for value in values:
                        self.extensions_document.append(value.strip())
