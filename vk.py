import time
import requests

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# browser options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument("--no-sandbox")  # Обход песочницы
chrome_options.add_argument("--disable-dev-shm-usage")  # Использование разделяемой памяти
chrome_options.add_argument("--disable-gpu")  # Отключение GPU (для совместимости)
chrome_options.add_argument('--headless')  # Режим без графического интерфейса
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(1)
# - - -

driver.get('https://vk.com/clips/parapa_official')


async def offset_clips():
    el_clip = driver.find_element(By.XPATH, '(//a[@data-testid="clip-preview"])[last()]')
    clip = el_clip.get_attribute('href')
    ActionChains(driver).scroll_to_element(el_clip).perform()
    time.sleep(5)
    return clip


async def get_short_video(data):
    count = []
    views = []
    comments = []
    likes = []

    token_vk = ('vk1.a.2ShG8XrDz-MoGqQEcPy6Us3XlFpXZkEkKDR6Z11VxmoHL7E0Eo3oxiTNzQUYWj'
                '-VxXhOnhpKHLOYTwDIIakw_336tjKEoo1Duuyri8QfjxYzJa4Gc5TmtO7QP3ohOJ9hkTvCU_z7uzGQizuQHtLB_JURm8o6SSpYE9B9ZGxh-N9kuyMvZ5jdj7Wr0echGPxCruUcoAKIdplt6vGWv1nAjQ')

    r = requests.get(
        f'https://api.vk.com/method/video.get?videos={','.join(data[:200])}&count=200&v=5.131&access_token={token_vk}').json()

    for item in r.get('response').get('items'):
        if item.get('type') == 'short_video':
            count.append(item.get('type'))
            views.append(item.get('views'))
            comments.append(item.get('comments'))
            likes.append(item.get('likes').get('count'))

    return [len(count), sum(views), sum(comments), sum(likes)]


async def main():
    first_clip = driver.find_element(By.XPATH, '(//a[@data-testid="clip-preview"])[1]').get_attribute('href')
    last_clip = await offset_clips()
    next_clip = await offset_clips()

    while next_clip != last_clip:
        last_clip = next_clip
        next_clip = await offset_clips()

    first_clip = int(first_clip.split('clip')[-1].split('_')[-1])
    last_clip = int(last_clip.split('clip')[-1].split('_')[-1])

    result = []

    for i in range(last_clip, first_clip + 1):
        result.append(f'-41100567_{i}')

    count = 0
    views = 0
    comments = 0
    likes = 0

    while len(result) > 0:
        result_offset = await get_short_video(result)
        count = count + result_offset[0]
        views = views + result_offset[1]
        comments = comments + result_offset[2]
        likes = likes + result_offset[3]
        result = result[200:]

    print('count', count)
    print('views', views)
    print('comments', comments)
    print('likes', likes)

    return [count, views, comments, likes]
