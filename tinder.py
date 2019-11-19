try:
    import traceback
    import webbrowser
    import time
    import requests
    from bs4 import BeautifulSoup as bs
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except:
    print('import error:', traceback.format_exc())

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

base_url = 'https://tinder.com/app/likes-you/'
start_url ='https://tinder.com/app/recs'



def login_and_get_data():
    global driver
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--user-data-dir=chrome-data")
        driver = webdriver.Chrome('chromedriver.exe',
                                  options=chrome_options)
        session = requests.Session()
        request = session.get(start_url, headers=headers) # first argument = base_url ?
        driver.get('https://tinder.com/app/recs')
        if (request.status_code == 200):
            element_present = EC.presence_of_element_located((By.XPATH, "//html[@class='Expand Us(n) js-focus-visible']"))
            WebDriverWait(driver, 10).until(element_present)
            element_present = EC.presence_of_element_located((By.XPATH, "//div[@class='StretchedBox CenterAlign']"))
            if (driver.current_url != start_url):
                print('You have 80 seconds to log in')
                WebDriverWait(driver, 80).until(element_present)
            print('You have successfully logged in')
            WebDriverWait(driver, 10).until(element_present)
            html = driver.execute_script("return document.documentElement.outerHTML;")
            print(html)
            result = driver.find_element_by_xpath(
                "//a[@class='matchListItem D(ib) Pos(r) Ta(c) H(120px) H(180px)--m W(100%) Trsdu($normal) Wc($transform) Scale(1.1):h Op(1):h Mx(0)!']")
            result.click()
            element_present = EC.presence_of_element_located((By.XPATH, "//div[@class='Bdrs(8px) Bgz(cv) Bgp(c) Ov(h) StretchedBox Cnt($blank)::a StretchedBox::a Bg($inherit)::a Scale(1.3)::a Scale(1.2)::a--s Blur(12px)::a']"))
            WebDriverWait(driver, 10).until(element_present)
            result2 = driver.find_element_by_xpath(
                "//body[@class='M(0) Pos(f) Ov(h) P(0) Expand Fz($s) C($c-base) Ovsby(n)']")
            result2.click()
            result2.send_keys(Keys.END)
            element_present = EC.presence_of_element_located((By.XPATH,
                                                              "//div[@class='Bdrs(8px) Bgz(cv) Bgp(c) Ov(h) StretchedBox Cnt($blank)::a StretchedBox::a Bg($inherit)::a Scale(1.3)::a Scale(1.2)::a--s Blur(12px)::a']"))
            WebDriverWait(driver, 10).until(element_present)
            time.sleep(1)
            result2.send_keys(Keys.END)
            result2.send_keys(Keys.END)
            time.sleep(1)
        else:
            print('error. contact developer')
        html = driver.execute_script("return document.documentElement.outerHTML;")
        print(html)
        print(driver.get_cookies())
        driver.quit()
        return html
    finally:
        driver.quit()



def parse_and_open(html):
    soup = bs(html, 'html.parser')
    list_of_divs = []
    list_of_links = []
    results = soup.find_all('div', attrs={'class': 'Expand enterAnimationContainer'})
    for result in results:
        div = result.find('div').get('style')
        list_of_divs.append(div)
    for div in list_of_divs:
        list_of_links.append(div.split(r'"')[1])
    for link in list_of_links:
        webbrowser.open(url=link)

try:
    html = login_and_get_data()
    parse_and_open(html)
except:
    print('error: ', traceback.format_exc())
