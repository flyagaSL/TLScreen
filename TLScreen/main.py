import os
import time
import uuid
import sys
from config import Config
from logger import log
from selenium import webdriver
from PIL import ImageGrab
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


URL = "https://web.telegram.org/#/im"


def create_firefox_profile(conf):
    fp = webdriver.FirefoxProfile(conf.firefox_profile)
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir",
                      "{}TmpDownload".format(conf.download_folder))
    fp.set_preference("browser.helperApps.alwaysAsk.force", False)
    fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                      "application/octet-stream")
    return fp


def screen_object_profile(driver, conf):
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[1]")))

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
    img.save(conf.download_folder + 'profile.jpg')
    log.info("Сделан снимок профиля profile.jpg")

    button_active_sessions.click()

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[6]/div[2]/div/div/div[2]/div/div/div[1]/ul")))
    log.info("Загружены активные сессии профиля")

    img = ImageGrab.grab()
    img.save(conf.download_folder + 'active_sessions.jpg')
    log.info("Сделан снимок активных сессий пользователя active_sessions.jpg")

    driver.find_element_by_xpath(
        "/html/body/div[6]/div[2]/div/div/div[1]/div[1]/div/a").click()
    driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]").click()


def screen_headers_chats(driver, conf):
    slider = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div")

    height_chats = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div").size["height"]

    slider_y_position = slider.location["y"]

    img = ImageGrab.grab()
    img.save(conf.download_folder + "chats_0.jpg")
    log.info("Сделан 0-й снимок заголовков чатов chats_0.jpg")

    count = 1

    while True:
        driver.execute_script(
            "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, height_chats * count * 0.9))  # 0.9 - 90% от высоты диалога

        if slider_y_position == slider.location["y"]:
            break

        slider_y_position = slider.location["y"]
        time.sleep(0.5)
        img = ImageGrab.grab()
        img.save(conf.download_folder + "chats_{}.jpg".format(count))
        log.info(
            f"Сделан {count}-й снимок заголовков чатов chats_{count}.jpg")
        count = count + 1

    driver.execute_script(
        "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, 0))


def screen_chat(driver, conf):
    chat_header = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div/div[2]/a")))
    chat_header.click()

    chat_type = driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[2]").text

    chat_name = driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[2]/div[2]/div[1]").text

    chat_status = driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]").text

    path_chat_folder = "{}{}".format(conf.download_folder, chat_name)

    if os.path.isdir(path_chat_folder):
        path_chat_folder = path_chat_folder + "_{}".format(uuid.uuid4())

    path_chat_folder = path_chat_folder + "\\"

    os.mkdir(path_chat_folder)
    log.info("Создана папка path_chat_folder")

    img = ImageGrab.grab()
    img.save(path_chat_folder + "profile.jpg")
    log.info(
        f"Сделан снимок профиля собеседника {path_chat_folder}profile.jpg")

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
    img.save(path_chat_folder + "chat_0.jpg")
    log.info(f"Сделан 0-й снимок диалога {path_chat_folder}chat_0.jpg")

    screen_number = 1
    while True:
        scroll_height = chat_height * screen_number * 0.9
        driver.execute_script(
            "document.getElementsByClassName(\"im_history_scrollable_wrap\")[0].scroll({}, {})".format(0, scroll_height))
        time.sleep(0.5)
        img = ImageGrab.grab()
        img.save(path_chat_folder + "\\chat_{}.jpg".format(screen_number))
        log.info(f"{path_chat_folder}\chat_{screen_number}.jpg")

        if scroll_height >= hystory_chat.size["height"]:
            break
        screen_number = screen_number + 1

    log.info("Начало загрузки вложений")
    audios = driver.find_elements_by_css_selector(
        "div.im_history_messages_peer:not(.ng-hide) div.audio_player_actions > a:nth-child(1)")

    for download_audio in audios:
        download_audio.click()

    documents = driver.find_elements_by_css_selector(
        "div.im_history_messages_peer:not(.ng-hide) .im_message_document")

    download_documents = 0
    for document in documents:
        extension_document = document.find_element_by_xpath(".").find_element_by_class_name(
            "im_message_document_name").get_attribute("data-ext")

        if extension_document in conf.extensions_document:
            document.find_element_by_css_selector(
                "div.im_message_document_actions > a:nth-child(1)").click()
            download_documents = download_documents + 1

    count_documents = len(audios) + download_documents
    while True:
        if len(os.listdir("{}TmpDownload".format(conf.download_folder))) == count_documents:
            log.info(f"Загружено {count_documents} документов")
            break
        else:
            time.sleep(0.5)

    for file in os.listdir("{}TmpDownload".format(conf.download_folder)):
        os.rename("{}TmpDownload\\{}".format(conf.download_folder, file),
                  path_chat_folder + "\\{}".format(file))
    log.info(f"Загруженные файлы перемещены в {path_chat_folder}")


def screen_chats(driver, conf):
    if not os.path.isdir("{}TmpDownload".format(conf.download_folder)):
        os.mkdir("{}TmpDownload".format(conf.download_folder))
        log.info(f"папка {conf.download_folder}TmpDownload создана")
    chat_number = 0
    while True:
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
        screen_chat(driver, conf)


if __name__ == "__main__":
    log.info("Начало выполнения программы")
    log.info("Анализ конфиг файла")
    conf = Config()
    conf.parse_config("config.txt")
    driver = webdriver.Firefox(create_firefox_profile(conf))
    log.info("Профиль firefox успешно настроен")
    wait = WebDriverWait(driver, 50)
    driver.get(URL)
    screen_object_profile(driver, conf)
    screen_headers_chats(driver, conf)
    screen_chats(driver, conf)
    log.info("Выполнение программы успешно завершено!!!")
