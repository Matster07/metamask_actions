import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import cprint

PASSWORD = '123456789'
DELAY_BEFORE_ACTIONS = 1

def login(driver, password):
    # Пароль
    inputTextXpath(driver, DELAY_BEFORE_ACTIONS, password, '/html/body/div[1]/div/div[2]/div/div/form/div/div/input')

    # Продолжить
    clickOnXpath(driver, DELAY_BEFORE_ACTIONS, '/html/body/div[1]/div/div[2]/div/div/button')

def give_permission_to_site(driver):
    # Выбор счета
    clickOnXpath(driver, DELAY_BEFORE_ACTIONS, '/html/body/div[1]/div/div[2]/div/div[3]/div[2]/button[2]')

    # Подключиться
    clickOnXpath(driver, DELAY_BEFORE_ACTIONS, '/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]')

def approve_transaction(driver):
    # Подтвердить транзакцию
    clickOnXpath(driver, DELAY_BEFORE_ACTIONS, '/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]')

def clickOnXpath(driver, wait_time, str_path):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, str_path))).click()

def clickOnClassName(driver, wait_time, str_path):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.CLASS_NAME, str_path))).click()

def clickOnID(driver, wait_time, str_path):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.ID, str_path))).click()

def inputTextXpath(driver, wait_time, send_data, str_path):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, str_path))).send_keys(send_data)

def inputTextName(driver, wait_time, send_data, str_path):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.NAME, str_path))).send_keys(send_data)

def inputTextClassName(driver, wait_time, send_data, str_path):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.CLASS_NAME, str_path))).send_keys(send_data)

def inputTextByID(driver, wait_time, send_data, str_path):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.ID, str_path))).send_keys(send_data)

def waitElementXpath(driver, wait_time, str_path):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, str_path)))

def waitElementID(driver, wait_time, str_path):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, str_path)))


def line_control(file_txt):
    # Удаление пустых строк
    with open(file_txt) as f1:
        lines = f1.readlines()
        non_empty_lines = (line for line in lines if not line.isspace())
        with open(file_txt, "w") as n_f1:
            n_f1.writelines(non_empty_lines)

def main(ads_id, password):
    try:
        open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
        close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id

        try:
            # Отправка запроса на открытие профиля
            resp = requests.get(open_url).json()
        except requests.exceptions.ConnectionError:
            cprint(f'adspover is not running', 'white')
            exit(0)

        chrome_driver = resp["data"]["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])

        with webdriver.Chrome(service=Service(chrome_driver), options=chrome_options) as driver:
            number_windows = len(driver.window_handles)

            while True:
                try:
                    time.sleep(1)

                    if number_windows + 1 == len(driver.window_handles):
                        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])

                    number_windows = len(driver.window_handles)

                    print(driver.current_url)

                    if driver.current_url.find('#unlock'):
                        # Пароль и продолжить
                        login(driver, password)

                        # Выбор счета и подключиться
                        give_permission_to_site(driver)
                    elif driver.current_url.find('#connect') != -1:
                        # Выбор счета и подключиться
                        give_permission_to_site(driver)
                    elif driver.current_url == 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/notification.html':
                        # Подтверждение транзакцию
                        approve_transaction(driver)

                except Exception:
                        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])

    except Exception as ex:
        # traceback.print_exc()
        driver.quit()
        driver.get(close_url)
        cprint(f'{zero + 1}. {ads_id} = already done', 'yellow')

if __name__ == '__main__':

    line_control("id_users.txt")

    with open("id_users.txt", "r") as f:
        id_users = [row.strip() for row in f]

    for ads_id in id_users:
        main(ads_id, PASSWORD)