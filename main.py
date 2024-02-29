from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import schedule
import time
import sys

url = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do?t_s=1709183352309#/sportVenue'
chromedriver = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"    # 需要填入自己电脑chromedriver的地址
driver = webdriver.Chrome(executable_path=chromedriver)

# 以下是必填的信息
username = "XXXXXXXXXX"             # 深圳大学统一认证的账号
password = "XXXXXXXXXX"             # 深圳大学统一认证的密码
appointment = 'XX:00-XX:00(可预约)'  # 想要预约的时间,格式为'XX:00-XX:00(可预约)',如'08:00-09:00(可预约)'或'18:00-19:00(可预约)'
payment_password = 'XXXXXXXXXX'     # 支付体育经费的密码
companions_id = ['XXXXXXXXXX']      # 同行人的校园卡号或学号，可填多个同行人，格式为['XXXXXXXXXX','XXXXXXXXXX',……]


def Login():
    """登录"""
    driver.get(url)
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_class_name("auth_login_btn").click()
    time.sleep(5)

def Select():
    """选择时间并从可选的球场中选场"""
    driver.find_element_by_xpath("//div[text()='粤海校区']").click()
    time.sleep(1)

    driver.find_element_by_xpath("//div[text()='羽毛球']").click()
    time.sleep(2)

    driver.find_element_by_xpath("//div[@class='ellipse-5']").click()

    driver.find_element_by_xpath(f"//div[text()='{appointment}']").click()
    time.sleep(1)

    buttons = driver.find_elements(By.CSS_SELECTOR, ".group-2")
    for button in buttons:
        if ("可预约" in button.text) and ("羽毛球场" in button.text):
            button.click()
            break

    driver.find_element_by_xpath("//button[text()='提交预约']").click()
    time.sleep(8)

def Add_companions():
    """添加同行人"""
    driver.find_element_by_xpath("//a[text()='同行人']").click()
    time.sleep(1)

    for companion_id in companions_id:
        driver.find_element_by_xpath("//button[text()='添加同行人']").click()
        time.sleep(1)

        driver.find_element_by_id("searchId").send_keys(companion_id)
        driver.find_element_by_xpath("//div[text()='查询']").click()
        time.sleep(3)

        driver.find_element_by_xpath("//button[text()='确定']").click()
        time.sleep(1)

    driver.find_element(By.CLASS_NAME, "jqx-window-close-button").click()
    time.sleep(1)

def Pay():
    """通过体育经费支付"""
    driver.find_element_by_xpath("//a[text()='未支付']").click()
    time.sleep(1)

    try:
        button = driver.find_element_by_xpath("//button[text()='(体育经费)支付']")
        button.click()
    except NoSuchElementException:
        button = driver.find_element_by_xpath("//button[text()='(剩余金额)支付']")
        button.click()
        return
    time.sleep(8)

    # 切换到支付窗口
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    driver.find_element_by_id("btnNext").click()
    time.sleep(1)

    driver.find_element_by_id("password").click()
    time.sleep(1)

    for ele in payment_password:
        driver.find_element(By.CLASS_NAME, f"key-button.key-{ele}").click()

    driver.find_element_by_xpath("//button[text()='确认支付']").click()
    time.sleep(1)

def Work():
    Login()
    Select()
    Add_companions()
    Pay()
    print('预约并支付成功')
    sys.exit()

schedule.every().day.at("12:00").do(Work)   # 12:00自动开始预约

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)





