from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import schedule
import time
import sys
import os

url = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do?t_s=1709183352309#/sportVenue'
chromedriver = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"    # 需要填入自己电脑chromedriver的地址
driver = webdriver.Chrome(executable_path=chromedriver)
next_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.now().strftime('%Y-%m-%d')

# 以下是必填的信息
chromedriver = "XXXXXXXXXX"    # 需要填入自己电脑chromedriver的地址
username = "XXXXXXXXXX"             # 深圳大学统一认证的账号
password = "XXXXXXXXXX"             # 深圳大学统一认证的密码
campus = "XXXXXXXXXX"
ball = "XXXXXXXXXX"
appointment = 'XXXXXXXXXX'  # 想要预约的时间,格式为'XX:00-XX:00(可预约)',如'08:00-09:00(可预约)'或'18:00-19:00(可预约)'
venues = "XXXXXXXXXX"
payment_password = 'XXXXXXXXXX'     # 支付体育经费的密码
companions_id = []      # 同行人的校园卡号或学号，可填多个同行人，格式为['XXXXXXXXXX','XXXXXXXXXX',……]，列表为空则不添加同行人


def Login():
    """登录"""
    driver.get(url)

    # 查找用户名输入框并输入用户名
    # wait = WebDriverWait(driver, 10)
    # username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    # username_input.send_keys(username)

    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "username"))
    )
    username_input.send_keys(username)

    # 使用JavaScript将变量 password 的值输入到密码框中
    driver.execute_script("document.getElementById('password').value=arguments[0];", password)

    # 确保密码框的值已经更新为你输入的密码
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.ID, "password"), password)
    )

    # 等待登录按钮加载最多10秒并点击
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login_submit"))
    )
    driver.execute_script("arguments[0].click();", login_button)

def Select():
    """选择时间并从可选的球场中选场"""

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[text()='{campus}']")))
    element.click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[text()='{ball}']")))
    element.click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='{next_day}']")))
    element.click()

    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[text()='{appointment}']")))
        element.click()
    except TimeoutException:
        # 如果因为超时而未找到元素，则打印提示信息并退出程序
        print("该时间段没场了")
        sys.exit(1)

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[text()='{venues}']")))
    element.click()

    group_2_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'group-2')))
    for group_2 in group_2_elements:
        element = group_2.find_element(By.CLASS_NAME, 'element')
        if '可预约' in element.text and '场' in element.text:
            frame_child1 = group_2.find_element(By.CLASS_NAME, 'frame-child1')
            frame_child1.click()
            break

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='提交预约']")))
    element.click()

def Add_companions():
    """添加同行人"""
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='同行人']")))
    element.click()

    for companion_id in companions_id:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='添加同行人']")))
        element.click()
        time.sleep(1)

        driver.find_element_by_id("searchId").send_keys(companion_id)
        driver.find_element_by_xpath("//div[text()='查询']").click()

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='确定']")))
        element.click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jqx-window-close-button")))
    element.click()

def Pay():
    """通过体育经费支付"""
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='未支付']")))
    element.click()

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

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.ID, "btnNext")))
    element.click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    element.click()

    time.sleep(1)
    for ele in payment_password:
        driver.find_element(By.CLASS_NAME, f"key-button.key-{ele}").click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='确认支付']")))
    element.click()

def Work():
    Login()
    Select()
    if companions_id:
        Add_companions()
    if payment_password:
        Pay()
    print('预约并支付成功')


def check_time_and_run():
    current_time = datetime.now().time()
    target_time = datetime.strptime("12:30:00", "%H:%M:%S").time()
    if current_time >= target_time:
        return True
    else:
        return False

if __name__ == "__main__":
    # 创建字典来存储配置信息
    config = {}

    # 读取同目录下的 information.txt 文件
    with open("information.txt", "r", encoding="utf-8") as f:
        for line in f:
            # 去掉首尾的空白字符，并跳过空行或注释行
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # 分割键和值
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    # 解析配置信息
    chromedriver = config.get("chromedriver")
    username = config.get("username")
    password = config.get("password")
    campus = config.get("campus")
    ball = config.get("ball")
    appointment = config.get("appointment")
    venues = config.get("venues")
    payment_password = config.get("payment_password")

    # 处理同行人 ID，分割并去除空白字符
    companions_id = [id.strip() for id in config.get("companions_id", "").split(",") if id.strip()]

    # 检查配置是否正确加载
    print("chromedriver路径:", chromedriver)
    print("用户名:", username)
    print("密码:", password)
    print("校区:", campus)
    print("球类:", ball)
    print("预约时间:", appointment)
    print("场馆:", venues)
    print("支付密码:", payment_password)
    print("同行人id:", companions_id)

    while True:
        if check_time_and_run():
            Work()
            break
        else:
            time.sleep(1)
    sys.exit()



