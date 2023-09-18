import time
from datetime import datetime

from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from com.SendMailUtil import SendMail
from com.models import GroupMember
from db.dao import get_groups, save_member, set_group_crawled
from utils import convert_to_date

etree = html.etree


def parser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def login(gid):
    url = f"https://qun.qq.com/member.html#gid={gid}"
    driver = parser()
    driver.get(url)
    time.sleep(8)

    scroll_left_to_bottom(driver)
    page_source = driver.page_source
    get_data(page_source, gid)

    return driver


def extract_group_info(fullname: str) -> (str, int):
    group_name = fullname.split('(')[0]
    group_id = int(fullname.split('(')[1].split(')')[0])
    return group_name, group_id


def get_data(page_source, gid):
    html = etree.HTML(page_source)
    mem_info_list = html.xpath('//*[@id="groupMember"]/tbody[@class="list"]/tr')

    members = []
    for mem_info in mem_info_list:
        nickname = str(mem_info.xpath('./td[3]/span/text()')[0]).strip()
        qq = int(str(mem_info.xpath('./td[5]//text()')[0]).strip())
        gender = str(mem_info.xpath('./td[6]//text()')[0]).strip()
        qq_age = str(mem_info.xpath('./td[7]//text()')[0]).strip()
        joint_at = str(mem_info.xpath('./td[8]//text()')[0]).strip()
        last_active_at = str(mem_info.xpath('./td[9]//text()')[0]).strip()

        member = GroupMember(
            nickname=nickname,
            qq=qq,
            gender=gender,
            qq_age=qq_age,
            qq_created_at=convert_to_date(qq_age),
            joint_at=datetime.strptime(joint_at, "%Y/%m/%d"),
            last_active_at=datetime.strptime(last_active_at, "%Y/%m/%d"),
            gid=int(gid),
        )

        save_member(member)


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


if __name__ == '__main__':
    groups = get_groups()
    for group in groups:
        print(f"Please login with your QQ: {group.login_qq}")
        login(group.gid)
        set_group_crawled(group.gid)
        time.sleep(3)
