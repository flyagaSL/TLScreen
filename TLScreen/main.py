'''
:copyright: (c) 2020 by lavrovsergei97
:license: Apache2, see LICENSE for more details.
'''

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
import time
import uuid
import sys
import urllib.request
from config import Config
from logger import log
from selenium import webdriver
from PIL import ImageGrab
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

URL = "https://web.telegram.org/#/im"


# Проверка интернет соединения. Функция будет бесконечно ожидать подключения к интернету
def check_internet_connection():
    try:
        urllib.request.urlopen("http://google.com")
    except IOError:
        log.info("Ожидается интернет соединение")
        time.sleep(1)
        check_internet_connection()
    else:
        log.info("Интернет соединение установлено")


# Настройка профиля браузера, под которым будет выполняться программа. (настроенный профиль)
def create_firefox_profile(conf):
    fp = webdriver.FirefoxProfile(conf.firefox_profile)
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", os.path.join(conf.download_folder, "TmpDownload"))
    fp.set_preference("browser.helperApps.alwaysAsk.force", False)
    fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                      "application/octet-stream;audio/ogg;audio/mpeg")
    return fp


# Проверка на успешный вход (0: вход успешно выполнен; -1: ошибка)
def check_login():
    if driver.current_url != URL:
        driver.get(URL)
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[1]")))
    except TimeoutException:
        if driver.current_url == 'https://web.telegram.org/#/login':
            log.info("Вход в телеграм не выполнен")
        else:
            log.info(
                "Не удалось загрузить начальную страницу Telegram: https://web.telegram.org//#//im")
        return -1
    else:
        return 0


# Снимки всех чатов (0: снимки сделаны успешно; -1: ошибка)
def screen_chats(driver, conf):
    if check_login():
        return check_login
    if not os.path.isdir(os.path.join(conf.download_folder, "TmpDownload")):
        os.mkdir(os.path.join(conf.download_folder,"TmpDownload"))
        log.info(f"Папка {os.path.join(conf.download_folder, 'TmpDownload')} создана")
    

    def screen_chat():
        chat_header = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div/div[2]/a")))
        chat_header.click()

        chat_type = driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[2]").text

        chat_name = driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div/div[1]/div[2]/div[2]/div[1]").text

        chat_status = driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]").text

        path_chat_folder = os.path.join(conf.download_folder, chat_name)

        if os.path.isdir(path_chat_folder):
            path_chat_folder = path_chat_folder + f"_{uuid.uuid4()}"

        os.mkdir(path_chat_folder)
        log.info(f"Создана папка {path_chat_folder}")

        img = ImageGrab.grab()
        img.save(os.path.join(path_chat_folder, "profile.jpg"))
        log.info(
            f"Сделан снимок профиля собеседника {os.path.join(path_chat_folder, 'profile.jpg')}")

        driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a").click()

        if chat_status == "bot" and not conf.screen_bot:
            log.info(
                f"Чат с {chat_name} был пропущен из-за настройки в config: SCREEN_BOT: False")
            return

        if chat_type == "Group info" and not conf.screen_group:
            log.info(
                f"Чат с {chat_name} был пропущен из-за настройки в config: SCREEN_GROUP: False")
            return

        if chat_type == "Contact info" and not conf.screen_contact:
            log.info(
                f"Чат с {chat_name} был пропущен из-за настройки в config: SCREEN_CONTACT: False")
            return

        if chat_type == "Channel info" and not conf.screen_channel:
            log.info(
                f"Чат с {chat_name} был пропущен из-за настройки в config: SCREEN_CHANNEL: False")
            return

        hystory_chat = driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div")

        hystory_chat_height = hystory_chat.size["height"]

        # scount = 1
        while True:
            driver.execute_script(
                "document.getElementsByClassName(\"im_history_scrollable_wrap\")[0].scroll(0, 0)")
            time.sleep(0.5)
            try:
                WebDriverWait(driver, 40).until(EC.invisibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]")))
            except Exception as except_info:
                break

            num_messages = len(driver.find_elements_by_css_selector(
                "div.im_history_messages_peer:not(.ng-hide) > div.im_history_message_wrap"))

            if (hystory_chat_height == hystory_chat.size["height"]) or (conf.max_messages <= num_messages):
                break

            hystory_chat_height = hystory_chat.size["height"]

        chat_height = driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]").size["height"]

        img = ImageGrab.grab()
        img.save(os.path.join(path_chat_folder,"chat_0.jpg"))
        log.info(f"Сделан 0-й снимок диалога {os.path.join(path_chat_folder,'chat_0.jpg')}")

        screen_number = 1
        while True:
            scroll_height = chat_height * screen_number * 0.9
            driver.execute_script(
                "document.getElementsByClassName(\"im_history_scrollable_wrap\")[0].scroll({}, {})".format(0, scroll_height))
            time.sleep(0.5)
            img = ImageGrab.grab()
            img.save(os.path.join(path_chat_folder, f"chat_{screen_number}.jpg"))
            log.info(f"Сделан {screen_number}-й снимок диалога {os.path.join(path_chat_folder, f'chat_{screen_number}.jpg')}")

            if scroll_height >= hystory_chat.size["height"]:
                break
            screen_number = screen_number + 1

        log.info("Начало загрузки вложений")
        audios = driver.find_elements_by_css_selector(
            "div.im_history_messages_peer:not(.ng-hide) div.audio_player_actions > a:nth-child(1)")

        download_audios = 0
        for download_audio in audios:
            try:
                download_audio.click()
                download_audios = download_audios + 1
            except StaleElementReferenceException:
                log.info("Ошибка загрузки аудио сообщения")

        documents = driver.find_elements_by_css_selector(
            "div.im_history_messages_peer:not(.ng-hide) .im_message_document")

        download_documents = 0
        for document in documents:
            extension_document = document.find_element_by_xpath(".").find_element_by_class_name(
                "im_message_document_name").get_attribute("data-ext")

            if extension_document in conf.extensions_document:
                try:
                    document.find_element_by_css_selector(
                        "div.im_message_document_actions > a:nth-child(1)").click()
                    download_documents = download_documents + 1
                except StaleElementReferenceException:
                    log.info("Ошибка загрузки документа")

        count_documents = download_audios + download_documents
        while True:
            if len(os.listdir(os.path.join(conf.download_folder, "TmpDownload"))) == count_documents:
                log.info(f"Загружено {count_documents} вложений")
                break
            else:
                time.sleep(0.5)

        for file in os.listdir(os.path.join(conf.download_folder, "TmpDownload")):
            os.rename(os.path.join(conf.download_folder, "TmpDownload", file), os.path.join(path_chat_folder, file))
        log.info(f"Загруженные файлы перемещены в {path_chat_folder}")

    dialogs = driver.find_elements_by_class_name('im_dialog_wrap')

    chat_number = 0
    while chat_number < len(dialogs):
        chat_number = chat_number + 1

        badge_chat = driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]/a/div[1]/span".format(chat_number))

        if badge_chat.text != "" and not (conf.screen_unread_messages):
            log.info(
                f"Чат {chat_number} имеет непрочитанные сообщения и поэтому был пропущен")
            continue

        chat = driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]".format(chat_number))
        chat.click()
        screen_chat()
    return 0


# Снимки заголовком всех чатов (0: снимки сделаны успешно; -1: ошибка)
def screen_headers_chats(driver, conf):
    if check_login():
        return check_login

    slider = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div")

    height_chats = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div").size["height"]

    slider_y_position = slider.location["y"]

    img = ImageGrab.grab()
    img.save(os.path.join(conf.download_folder,"chats_0.jpg"))
    log.info("Сделан 0-й снимок заголовков чатов chats_0.jpg")

    count = 1

    while True:
        driver.execute_script(
            "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, height_chats * count * 0.9))  # 0.9 - 90% от высоты диалога

        if slider_y_position == slider.location["y"]:
            break

        slider_y_position = slider.location["y"]

        # 0.7 секунд ждать для прогрузки диалогов. Число подобрано экспериментальным путём.
        time.sleep(0.7)

        img = ImageGrab.grab()
        img.save(os.path.join(conf.download_folder, f"chats_{count}.jpg"))
        log.info(
            f"Сделан {count}-й снимок заголовков чатов chats_{count}.jpg")
        count = count + 1

    driver.execute_script(
        "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, 0))

    return 0

# Снимки основного профиля (0: снимки сделаны успешно; -1: ошибка)


def screen_object_profile(driver, conf):
    if check_login():
        return check_login

    button_menu = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/a/div")))

    button_menu.click()
    log.info("Переход в меню профиля")

    button_settings = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/ul/li[3]/a")))

    button_settings.click()
    log.info("Переход в настройки профиля")

    button_active_sessions = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[5]/div[2]/div/div/div[3]/div/div[4]/div[3]/a")))

    if not os.path.isdir(conf.download_folder):
        os.mkdir(conf.download_folder)
        log.info(f"Создана папка {conf.download_folder}")

    img = ImageGrab.grab()
    img.save(os.path.join(conf.download_folder, 'profile.jpg'))
    log.info("Сделан снимок профиля profile.jpg")

    button_active_sessions.click()

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[6]/div[2]/div/div/div[2]/div/div/div[1]/ul")))
    log.info("Загружены активные сессии профиля")

    img = ImageGrab.grab()
    img.save(os.path.join(conf.download_folder,'active_sessions.jpg'))
    log.info("Сделан снимок активных сессий пользователя active_sessions.jpg")

    driver.find_element_by_xpath(
        "/html/body/div[6]/div[2]/div/div/div[1]/div[1]/div/a").click()
    driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]").click()
    return 0


if __name__ == "__main__":
    start_time = time.time()
    log.info("Начало выполнения программы")
    log.info("Разбор конфиг файла config.txt")
    conf = Config()
    conf.parse_config("config.txt")
    driver = webdriver.Firefox(
        executable_path=conf.geckodriver,  firefox_profile=create_firefox_profile(conf))
    log.info("Профиль firefox успешно настроен")
    conf.print_parametrs()
    check_internet_connection()
    wait = WebDriverWait(driver, 40)
    driver.get(URL)
    if screen_object_profile(driver, conf):
        driver.close()
        sys.exit()
    else:
        log.info("Снимки профиля выполнены")
    if screen_headers_chats(driver, conf):
        driver.close()
        sys.exit()
    else:
        log.info("Снимки заголовков чатов выполнены")
    if screen_chats(driver, conf):
        driver.close()
        sys.exit()
    else:
        driver.close()
        log.info("Снимки чатов выполнены")
        log.info(
            f"Выполнение программы успешно завершено!!! Время выполнения: {time.time() - start_time} с.")
