import os
import time
from selenium import webdriver
from PIL import ImageGrab
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

DOWNLOAD_FOLDER = "D:\\Programs\\TLScreen\\TLScreen\\Telegram\\"

MAX_MESSAGES = 1000

url = "https://web.telegram.org/#/im"
fp = webdriver.FirefoxProfile(os.environ["MProfile"])
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir",
                  "{}TmpDownload".format(DOWNLOAD_FOLDER))
fp.set_preference("browser.helperApps.alwaysAsk.force", False)


driver = webdriver.Firefox(fp)

wait = WebDriverWait(driver, 20)

driver.get(url)

chats = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[1]")))

button_menu = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/a/div")))

button_menu.click()

button_settings = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/ul/li[3]/a")))

button_settings.click()

button_active_sessions = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[5]/div[2]/div/div/div[3]/div/div[4]/div[3]/a")))

if not os.path.isdir(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)

img = ImageGrab.grab()
img.save(DOWNLOAD_FOLDER + 'profile.jpg')

button_active_sessions.click()

active_sessions = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[6]/div[2]/div/div/div[2]/div/div/div[1]/ul")))

img = ImageGrab.grab()
img.save(DOWNLOAD_FOLDER + 'active_essions.jpg')

driver.find_element_by_xpath(
    "/html/body/div[6]/div[2]/div/div/div[1]/div[1]/div/a").click()
driver.find_element_by_xpath(
    "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]").click()

slider = driver.find_element_by_xpath(
    "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div")

height_chats = driver.find_element_by_xpath(
    "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]").size["height"]

slider_y_position = slider.location["y"]

img = ImageGrab.grab()
img.save(DOWNLOAD_FOLDER + "chats_0.jpg")


count = 1

'''
while True:
    print(height_chats * count)
    driver.execute_script(
        "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, height_chats * count * 0.9))  # 70% от высоты диалога

    print("old: {} new: {}".format(slider_y_position, slider.location["y"]))

    if slider_y_position == slider.location["y"]:
        break

    slider_y_position = slider.location["y"]
    time.sleep(0.5)
    img = ImageGrab.grab()
    img.save(DOWNLOAD_FOLDER + "chats{}.jpg".format(count))
    count = count + 1
'''


driver.execute_script(
    "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, 0))

chat_number = 0


while True:
    chat_number = chat_number + 1
    print("Выполненяется диалог: {}".format(chat_number))

    badge_chat = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]/a/div[1]/span".format(chat_number))

    if badge_chat.text != "":
        continue

    chat = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]".format(chat_number))
    chat.click()
    chat_header = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div/div[2]/a")))
    chat_header.click()

    chat_name = driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[2]/div[2]/div[1]").text

    path_chat_folder = "{}{}\\".format(
        DOWNLOAD_FOLDER, chat_name)

    if os.path.isdir(path_chat_folder):
        path_chat_folder = path_chat_folder + "_{}".format(chat_number)

    os.mkdir(path_chat_folder)

    img = ImageGrab.grab()
    img.save(path_chat_folder + "profile.jpg")

    driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a").click()

    slider_chat = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[2]/div")
    slider_chat_y = slider_chat.location["y"]

    hystory_chat = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div")

    hystory_chat_height = hystory_chat.size["height"]

    # scount = 1
    while True:
        driver.execute_script(
            "document.getElementsByClassName(\"im_history_scrollable_wrap\")[0].scroll(0, 0)")
        time.sleep(0.5)
        try:
            progress = WebDriverWait(driver, 40).until(EC.invisibility_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]")))
        except Exception as except_info:
            print(except_info)
            break

        num_messages = len(driver.find_elements_by_css_selector(
            "div.im_history_messages_peer:not(.ng-hide) > div.im_history_message_wrap"))

        if (hystory_chat_height == hystory_chat.size["height"]) or (MAX_MESSAGES <= num_messages):
            print("Старая высота {}   Новая высота {} Сообщений: {}".format(
                hystory_chat_height, hystory_chat.size["height"], num_messages))
            break

        hystory_chat_height = hystory_chat.size["height"]

    chat_height = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]").size["height"]

    img = ImageGrab.grab()
    img.save(path_chat_folder +
             "chat_0.jpg")
    screen_number = 1
    while True:
        scroll_height = chat_height * screen_number * 0.9
        driver.execute_script(
            "document.getElementsByClassName(\"im_history_scrollable_wrap\")[0].scroll({}, {})".format(0, scroll_height))

        time.sleep(0.5)
        img = ImageGrab.grab()
        img.save(path_chat_folder + "\\chat_{}.jpg".format(screen_number))

        if scroll_height >= hystory_chat.size["height"]:
            break
        screen_number = screen_number + 1

    audios = driver.find_elements_by_css_selector(
        "div.im_history_messages_peer:not(.ng-hide) div.audio_player_actions > a:nth-child(1)")

    for download_audio in audios:
        download_audio.click()

    documents = driver.find_elements_by_css_selector(
        "div.im_history_messages_peer:not(.ng-hide) div.im_message_document_actions > a:nth-child(1)")

    '''
    for document in documents:
        document.click()
    '''

    count_documents = len(audios)  # + len(documents)

    while True:
        if len(os.listdir("{}TmpDownload".format(DOWNLOAD_FOLDER))) == count_documents:
            break
        else:
            time.sleep(0.5)
    for document in os.listdir("{}TmpDownload".format(DOWNLOAD_FOLDER)):
        os.rename("{}TmpDownload\\{}".format(DOWNLOAD_FOLDER, document),
                  path_chat_folder + "\\{}".format(document))

print("Выполнение программы успешно завершено!!!")
