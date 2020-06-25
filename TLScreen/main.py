import os
import time
from selenium import webdriver
from PIL import ImageGrab
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCREEN_FOLDER = "Screenshots/"

url = "https://web.telegram.org/#/im"
fp = webdriver.FirefoxProfile(os.environ["MProfile"])

driver = webdriver.Firefox(fp)

wait = WebDriverWait(driver, 20)

driver.get(url)

dialogs = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//*[@id=\"ng-app\"]/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[1]")))

button_menu = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/a/div")))

button_menu.click()

button_settings = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/ul/li[3]/a")))

button_settings.click()

button_active_sessions = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[5]/div[2]/div/div/div[3]/div/div[4]/div[3]/a")))


img = ImageGrab.grab()
img.save(SCREEN_FOLDER + 'profile.jpg')

button_active_sessions.click()

active_sessions = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[6]/div[2]/div/div/div[2]/div/div/div[1]/ul")))

img = ImageGrab.grab()
img.save(SCREEN_FOLDER + 'activeSessions.jpg')

driver.find_element_by_xpath(
    "/html/body/div[6]/div[2]/div/div/div[1]/div[1]/div/a").click()
driver.find_element_by_xpath(
    "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]").click()

slider = driver.find_element_by_xpath(
    "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div")

height_dialogs = driver.find_element_by_xpath(
    "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]").size["height"]

print(height_dialogs)

slider_y_position = slider.location["y"]

img = ImageGrab.grab()
img.save(SCREEN_FOLDER + "dialogs0.jpg")


count = 1
while True:
    print(height_dialogs * count)
    driver.execute_script(
        "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, height_dialogs * count * 0.2))  # 30% от высоты диалога

    print("old: {} new: {}".format(slider_y_position, slider.location["y"]))

    if slider_y_position == slider.location["y"]:
        break

    slider_y_position = slider.location["y"]
    time.sleep(0.5)
    img = ImageGrab.grab()
    img.save(SCREEN_FOLDER + "dialogs{}.jpg".format(count))
    count = count + 1


driver.execute_script(
    "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, 0))

dialog_number = 0
while True:
    dialog_number = dialog_number + 1
    print("Выполненяется диалог: {}".format(dialog_number))
    badge_dialog = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]/a/div[1]/span".format(dialog_number))

    print(badge_dialog.text)

    if badge_dialog.text != "":
        continue

    dialog = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]".format(dialog_number))
    dialog.click()
    dialog_header = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div/div[2]/a")))
    dialog_header.click()

    img = ImageGrab.grab()
    img.save(SCREEN_FOLDER + "profile{}.jpg".format(dialog_number))

    driver.find_element_by_class_name('md_modal_action_close').click()
    time.sleep(0.5)

print("Выполнение программы успешно завершено!!!")
