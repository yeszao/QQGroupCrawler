import csv
import time
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from com.SendMailUtil import SendMail

etree = html.etree


def parser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def login(url, gid):
    driver = parser()
    driver.get(url)
    time.sleep(8)
    get_data(driver, gid)
    return driver


def get_data(driver, gid):
    scroll_left_to_bottom(driver)

    data = driver.page_source
    html = etree.HTML(data)
    group_title = html.xpath('//span[@id="groupTit"]/text()')
    mem_info_list = html.xpath('//*[@id="groupMember"]/tbody[@class="list"]/tr')  # TODO  QQ群成员列表

    with open(f'{gid}.csv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect="excel")
        writer.writerow(['成员', 'QQ号', '性别', 'Q龄', '入群时间', '最后发言'])

        for mem_info in mem_info_list:

            data = {'成员': str(mem_info.xpath('./td[3]//text()')[3]).replace('\U0001f60a', '').strip(),
                    'QQ号': str(mem_info.xpath('./td[5]//text()')[0]).replace('\U0001f60a', '').strip(),
                    '性别': str(mem_info.xpath('./td[6]//text()')[0]).replace('\U0001f60a', '').strip(),
                    'Q龄': str(mem_info.xpath('./td[7]//text()')[0]).replace('\U0001f60a', '').strip(),
                    '入群时间': str(mem_info.xpath('./td[8]//text()')[0]).replace('\U0001f60a', '').strip(),
                    '最后发言': str(mem_info.xpath('./td[9]//text()')[0]).replace('\U0001f60a', '').strip()}
            print(data)

            if data:
                # writer.writerow(['成员', 'QQ号', '性别', 'Q龄', '入群时间', '最后发言'])
                # writer.writerow(
                #     [data['成员'].replace('\xa0', ''), data['QQ号'].replace('\xa0', ''),
                #      data['性别'].replace('\xa0', ''), data['Q龄'].replace('\xa0', ''),
                #      data['入群时间'].replace('\xa0', ''), data['最后发言'].replace('\xa0', '')])
                writer.writerow(
                    [data['成员'], data['QQ号'],
                     data['性别'], data['Q龄'],
                     data['入群时间'], data['最后发言']])

                # 发送邮件
                #sendmail(data['QQ号'] + "@qq.com");


def scroll_left_to_bottom(driver):
    old_height = driver.execute_script("return document.body.scrollHeight;")
    while True:
        driver.execute_script(
            'window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"})')

        time.sleep(2.5)
        new_height = driver.execute_script("return document.body.scrollHeight;")
        if new_height == old_height:
            break

        old_height = new_height


def sendmail(user):
    SendMail().sendmail("are you ok", "最近过的还好吗，加我微信聊聊天吧WX666", user)


def logout(driver):
    # driver.find_element(By.CLASS_NAME, 'logout').click()
    # driver.close()需要在driver.quit()前面，因为driver.quit()方法会先关闭所有窗口并退出驱动，如果再次调用close则会报错
    driver.close()
    driver.quit()


def scroller(driver):
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)


def run(gid):
    url = "https://qun.qq.com/member.html#gid=" + gid
    login(url, gid)


if __name__ == '__main__':
    run('879813761')
