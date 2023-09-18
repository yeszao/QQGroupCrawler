import random
import time
from selenium.common.exceptions import NoSuchElementException

from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from com.SendMailUtil import SendMail
from com.models import GroupMember
from db.dao import save_member, set_group_crawled, get_or_add_group
from utils import convert_to_date, format_date

etree = html.etree


def parser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def login(start_qq: int):
    url = f"https://qun.qq.com/member.html"
    driver = parser()
    driver.get(url)
    time.sleep(8)

    # get groups
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ui-dialog on"]')))

    time.sleep(1)
    groups = get_groups(driver.page_source)
    new_groups = []
    for group in groups:
        new_groups.append(get_or_add_group(group, start_qq))

    for group in new_groups:
        if group.crawled:
            continue

        url = f"https://qun.qq.com/member.html#gid={group.gid}"
        driver.get(url)
        driver.refresh()
        scroll_to_bottom(driver)

        num, members = get_qq_members(driver.page_source)
        for member in members:
            save_member(member, group.gid)

        if len(members) >= num:
            set_group_crawled(group.gid)
            print(f"[{group.gid}] [{group.name}] [{len(members)}/{num}] crawled, SUCCESS.")
        else:
            print(f"[{group.gid}] [{group.name}] [{len(members)}/{num}] crawled, FAILED!")

        time.sleep(3)

    print("All done.")
    return driver


def get_groups(page_source):
    html = etree.HTML(page_source)
    xpaths = html.xpath('//ul[@class="my-group-list"]/li')

    groups = []
    for mem_info in xpaths:
        gid = int(str(mem_info.xpath('./@data-id')[0]).strip())
        group_name = str(mem_info.xpath('./@title')[0]).strip().replace('&nbsp;', ' ')
        groups.append({
            "gid": gid,
            "name": group_name
        })

    return groups


def get_qq_members(page_source) -> (int, list):
    html = etree.HTML(page_source)
    mem_info_list = html.xpath('//*[@id="groupMember"]/tbody[@class="list"]/tr')
    group_member_num = int(html.xpath('//span[@id="groupMemberNum"]/text()')[0])
    members = []

    for mem_info in mem_info_list:
        nickname = str(mem_info.xpath('./td[3]/span/text()')[0]).strip()
        qq = int(str(mem_info.xpath('./td[5]/text()')[0]).strip())
        gender = str(mem_info.xpath('./td[6]/text()')[0]).strip()
        qq_age = str(mem_info.xpath('./td[7]/text()')[0]).strip()
        joint_at = str(mem_info.xpath('./td[8]/text()')[0]).strip()
        last_active_at = str(mem_info.xpath('./td[last() - 1]/text()')[0]).strip()

        member = GroupMember(
            nickname=nickname,
            qq=qq,
            gender=gender,
            qq_age=qq_age,
            qq_created_at=convert_to_date(qq_age),
            joint_at=format_date(joint_at),
            last_active_at=format_date(last_active_at),
        )
        members.append(member)

    return group_member_num, members


def scroll_to_bottom(driver):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="groupMemberNum"]')))

    html = etree.HTML(driver.page_source)
    expected_num = int(html.xpath('//span[@id="groupMemberNum"]/text()')[0])

    while True:
        driver.execute_script('window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"})')
        time.sleep(random.randint(1, 3))

        try:
            driver.find_element(By.XPATH, f'//td[@class="td-no" and text() = "{expected_num}"]')
            break
        except NoSuchElementException as e:
            continue


def sendmail(user):
    SendMail().sendmail("are you ok", "最近过的还好吗，加我微信聊聊天吧WX666", user)


def logout(driver):
    # driver.find_element(By.CLASS_NAME, 'logout').click()
    # driver.close()需要在driver.quit()前面，因为driver.quit()方法会先关闭所有窗口并退出驱动，如果再次调用close则会报错
    driver.close()
    driver.quit()


if __name__ == '__main__':
    login(2956311905)
    # groups = get_groups()
    # for group in groups:
    #     print(f"Please login with your QQ: {group.login_qq}")
    #     login(group.gid)
    #     set_group_crawled(group.gid)
    #     time.sleep(3)
