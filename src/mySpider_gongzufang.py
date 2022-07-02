from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import conndb
from sendmail_for_gzf import sendmail


def start_selenium(url):
    option = webdriver.ChromeOptions()
    option.add_argument(r'--user-data-dir=C:\Users\hu765\AppData\Local\Google\Chrome\User Data\Default')
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    print("web握手成功")
    return driver


def get_house_content(driver):
    try:
        houses = driver.find_elements(By.CSS_SELECTOR, "[class='c-6 fs26']")  # 通过CSS selector获取对象
        pages = driver.find_elements(By.XPATH, "//ul[@class='el-pager']/li")  # 获取pages
        i = 1
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        global houselist
        houselist = []
        #        print(len(pages))
        if len(pages) > 1:
            for p in range(len(pages)):
                for house in houses:
                    # 遍历房源列表写入数据库
                    houselist.append(house.text)
                    print("获取到{}条房源".format(i))
                    i += 1
                print("成功抓取第{}页".format(p + 1))
                driver.find_element(By.CSS_SELECTOR, "[class='btn-next']").click()
                time.sleep(5)
                houses = driver.find_elements(By.CSS_SELECTOR, "[class='c-6 fs26']")  # 获取下一页对象
        else:
            for house in houses:
                # 遍历房源列表写入数据库
                houselist.append(house.text)
                print("获取到{}条房源".format(i))
                i += 1

        if len(houselist) != 0:
            try:
                conn, cur = conndb.conn_db()  # open database
                print("数据库连接成功")
                process_content(dt, houselist, cur)  # insert data
                print("数据写入完成")
            except Exception as e:
                print("数据库连接失败：", e)
            finally:
                conndb.conn_close(conn, cur)
        else:
            print("没有抓取到房源信息")
    except Exception as e:
        print(e)
    finally:
        driver.quit()


# 数据处理函数并写入数据库
def process_content(time, houses, cur):
    print("准备写入数据……")
    for house in houses:
        sql1 = "SELECT house_id FROM myDjangoWebAppHouse2ID WHERE house_name='%s'" % house
        conndb.exe_query(cur, sql1)
        results = cur.fetchone()  # 获取id
        if results is not None:  # 查询房源名称是否已注册
            house_id = results[0]
            sql = "INSERT INTO myApp001_mydata(house_id,get_time,house_source)values (%s,'%s','%s')" % (
                house_id, time, house)  # 插入房源信息
            conndb.exe_update(cur, sql)
        else:
            print("发现新房源[{}]，准备注册入库".format(house))
            sql2 = "INSERT INTO myDjangoWebAppHouse2ID(house_name)values ('%s')" % house  # 注册房源信息
            conndb.exe_update(cur, sql2)
            sql1 = "SELECT house_id FROM myDjangoWebAppHouse2ID WHERE house_name='%s'" % house
            conndb.exe_query(cur, sql1)
            results = cur.fetchone()  # 获取id号
            house_id = results[0]
            sql = "INSERT INTO myApp001_mydata(house_id,get_time,house_source)values (%s,'%s','%s')" % (
                house_id, time, house)
            conndb.exe_update(cur, sql)  # 插入房源信息
    conndb.exe_commit(cur)


# 判断是否有关注房源，如果有发邮件
def checkbox_houses(checkbox_houselist):
    receiver = "332461600@qq.com"
    if len(checkbox_houselist) != 0:
        if set(checkbox_houselist).isdisjoint(set(houselist)):
            return
        else:
            print("检测到有关注的房源，开始发邮件……")
            sendmail("发现关注房源", receiver, list(set(checkbox_houselist).intersection(set(houselist))))


def main():
    print("程序执行开始")
    url = "https://select.pdgzf.com/villageLists"
    driver = start_selenium(url)
    get_house_content(driver)
    checkbox_houses(checkbox_houselist)
    print("程序执行结束")


checkbox_houselist = ["民生路318弄(馨澜公寓)"]
main()
