from selenium import webdriver

url = "https://web.telegram.org/#/im"
fp = webdriver.FirefoxProfile(
    r"C:\Users\Сергей\AppData\Roaming\Mozilla\Firefox\Profiles\py7jbs00.default")

driver = webdriver.Firefox(fp)
driver.get(url)
