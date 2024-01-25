import csv
import json
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 配置移动设备模拟
mobile_emulation = {
    "deviceMetrics": {"width": 430, "height": 932, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36"
}

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# 其他Selenium Wire选项
wire_options = {
    'disable_encoding': True  # 禁用请求编码
}

# 打开输出文件
output_file = open(r'C:\Users\Admin\Desktop\collected_data2.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(output_file)
# 写入标题行
writer.writerow(['sign', 'qid', 'password', 'sign2', 'qid2', 'loginName'])

# 读取CSV文件中的账户信息
with open(r'C:\Users\Admin\Desktop\dou\123.csv', newline='') as csvfile:
    accounts = csv.reader(csvfile)
    next(accounts)  # 跳过标题行

    for account in accounts:
        if len(account) != 2:
            continue  # 跳过格式错误的行

        # 创建WebDriver实例
        driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=wire_options)

        username, password = account

        # 访问登录页面
        driver.get(
            'https://m.zlong68.com/bbs/login/?show=login&from=ph-58.com&back=https%3A%2F%2Fph-58.com%2Fn%2F%23%2F')
        driver.implicitly_wait(20)

        # 根据移动版页面的元素结构更新XPath
        # 找到用户名和密码输入框并输入
        driver.find_element(By.XPATH, '//*[@id="inputAreatext"]').send_keys(username)
        driver.find_element(By.XPATH, '//*[@id="form-password"]/input').send_keys(password)
        driver.implicitly_wait(20)

        # 点击登录按钮
        login_button = driver.find_element(By.XPATH, '//*[@id="login"]/div[4]/button')
        login_button.click()

        try:
            # 等待第一个接口请求完成
            driver.wait_for_request('/_glaxy_344a78_/customer/login', timeout=30)
            for request in driver.requests:
                if request.response and '/_glaxy_344a78_/customer/login' in request.url:
                    header_data = request.headers
                    body_data = json.loads(request.body.decode('utf-8'))
                    sign = header_data.get('sign')
                    qid = header_data.get('qid')
                    password = body_data.get('password')

            # 等待第二个接口请求完成
            driver.wait_for_request('/_glaxy_344a78_/_extra_/bbs/checkAndLoginV2', timeout=30)
            for request in driver.requests:
                if request.response and '/_glaxy_344a78_/_extra_/bbs/checkAndLoginV2' in request.url:
                    header_data2 = request.headers
                    body_data2 = json.loads(request.body.decode('utf-8'))
                    sign2 = header_data2.get('sign')
                    qid2 = header_data2.get('qid')
                    loginName = body_data2.get('loginName')

            # 将获取到的数据写入CSV文件
            writer.writerow([sign, qid, password, sign2, qid2, loginName])

        except TimeoutError:
            print("等待接口请求超时")

        # 关闭浏览器
        driver.quit()

# 关闭输出文件
output_file.close()

print("数据已保存到 collected_data2.csv")
