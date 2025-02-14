from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
from googletrans import Translator

import pytz
import os
import time


# Scroll to the bottom of the page to load older content for older post
def scroll_to_load(driver, max_scrolls=3):
    scroll_pause_time = 2  # Time to wait after each scroll
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_scrolls):
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        # Wait for the page to load and calculate the new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If the height hasn't changed, stop scrolling
            break
        last_height = new_height


def download_images(post_element, local_date):
    import os
    from urllib.request import urlretrieve

    # Create a directory for the images based on the date
    folder_path = f"images/{local_date}"
    os.makedirs(folder_path, exist_ok=True)

    # Locate the containers for the images
    image_containers = post_element.find_elements(By.CLASS_NAME, "bili-album__preview__picture")
    for index, container in enumerate(image_containers[:3]):  # Limit to 3 images
        try:
            # Locate the img tag within the container
            img_element = container.find_element(By.CSS_SELECTOR, "img")
            img_url = img_element.get_attribute("src")
            # Ensure the image URL is complete
            if img_url and img_url.startswith("//"):
                img_url = f"https:{img_url}"

            # Save the image locally
            file_path = os.path.join(folder_path, f"{index + 1}.jpg")
            urlretrieve(img_url, file_path)
            print(f"Downloaded image {index + 1} for {local_date}")
        except Exception as e:
            print(f"Failed to download image {index + 1} for {local_date}: {e}")


# Write to a file
def append_most_recent_post(file_path, date, link, title):
    """
    Appends the most recent post (date, link, title) to the end of the dynamics.txt file if not already present.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        existing_data = file.readlines()

    # Format the title to escape single quotes
    safe_title = title.replace('"', '\\"').replace("'", "\\'")
    json_line = f'{date}: ["{link}", "{safe_title}"]\n'

    # Append the new line to the file
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(json_line)
        print(f"Appended new post for {date} to {file_path}.")


def get_last_recorded_date(file_path):
    """Reads the last recorded date from the dynamics.txt file."""
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return None  # Return None if file does not exist or is empty

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            if ": " in last_line:
                return last_line.split(": ")[0]  # Extract the date part
    return None

options = Options()
options.add_argument("--headless")
# Set up the WebDriver for Firefox
service = Service("geckodriver.exe")  # Update this path to where your geckodriver is located
driver = webdriver.Firefox(service=service, options=options)
post_links = {}
find_same_old = False

try:
    # Open the Bilibili page
    url = "https://space.bilibili.com/57276677/dynamic"
    print("Debug: driver.get() the URl")
    driver.get(url)
    print("Debug: searching for posts")
    # Wait for the page to load
    driver.implicitly_wait(25)

    # COMMENT when automation
    # scroll_to_load(driver, max_scrolls=2)

    posts = driver.find_elements(By.CLASS_NAME, "bili-dyn-item")  # Fetch all posts
    local_date = datetime.now()
    cnt = 0
    for post in posts:
        # Dynamic Date
        cnt += 1
        print(f"Post {cnt} checked.")
        current_year = datetime.now().year
        try:
            dynamic_date_card = post.find_element(By.CLASS_NAME, "bili-dyn-item__desc")
        except NoSuchElementException:
            print("Skip Post")
            continue

        dynamic_date = str(dynamic_date_card.text)
        if len(dynamic_date) == 1:
            continue
        dynamic_type = str(dynamic_date_card.text.split(' ')[-1])  # jump video
        if dynamic_type[-2:] != "文章":
            continue

        # Dynamic ID
        dynamic_id_card = post.find_element(By.CLASS_NAME, "dyn-card-opus")
        dynamic_id = dynamic_id_card.get_attribute("dyn-id")

        # Dynamic Title
        dynamic_title = dynamic_id_card.text
        title_short = str(dynamic_title)[:25]

        # Check for the desired post title
        if "《日·键圈时刻表》" in title_short or "键圈时刻表" in title_short:
            # run at CHINA 10:30pm
            if "小时前" in str(dynamic_date) or "分钟前" in str(dynamic_date) \
                    or "今天" in str(dynamic_date):  # TODAY
                cur_time = datetime.now()
                localFormat = "%Y-%m-%d"
                tz = 'Asia/Shanghai'
                localDatetime = cur_time.astimezone(pytz.timezone(tz))
                local_date = local_date.strftime(localFormat)
            else:
                date_list = dynamic_date.split(' ')
                # special time
                if date_list[0] == "昨天" or date_list[0] == "前天":
                    cur_time = datetime.now()
                    localFormat = "%Y-%m-%d"
                    tz = 'Asia/Shanghai'
                    localDatetime = cur_time.astimezone(pytz.timezone(tz))
                    delta = 1 if date_list[0] == "昨天" else 2
                    local_date = localDatetime - timedelta(days=delta)
                    local_date = local_date.strftime(localFormat)
                # day amount
                elif date_list[0] == "2天前" or date_list[0] == "3天前":
                    cur_time = datetime.now()
                    localFormat = "%Y-%m-%d"
                    tz = 'Asia/Shanghai'
                    localDatetime = cur_time.astimezone(pytz.timezone(tz))
                    delta = 2 if date_list[0] == "2天前" else 3
                    local_date = localDatetime - timedelta(days=delta)
                    local_date = local_date.strftime(localFormat)
                # normal date
                else:
                    # Y-M-D
                    if len(date_list[0]) >= 11:
                        local_date = datetime.strptime(date_list[0], "%Y年%m月%d日").strftime("%Y-%m-%d")
                    else:  # M-D
                        local_date = datetime.strptime(date_list[0], "%m月%d日").strftime("%m-%d")
                        local_date = str(current_year) + '-' + local_date
            # title
            translator = Translator()
            title_content = dynamic_title.split("》")[1]
            title_content = title_content.split("\n")[0]
            translated_content = translator.translate(title_content, src="zh-CN", dest="en")

            # link
            post_links[local_date] = [f"https://www.bilibili.com/opus/{dynamic_id}", translated_content.text]
            print(f"Found: {local_date}")

        file_path = "dynamics.txt"
        last_recorded_date = get_last_recorded_date(file_path)
        find_same_old = last_recorded_date == local_date
        if find_same_old:
            print(f"No new post found; Last record: {last_recorded_date}")
        # download
        else:
            print(f"{local_date} Downloaded")
            download_images(post, local_date)
            append_most_recent_post(file_path, local_date, post_links[local_date][0], post_links[local_date][1])
        break

except Exception as e:
    print(f"Webpage Open Failed: {e}")

finally:
    # Close the browser
    driver.quit()
