from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains

from urllib.request import urlretrieve
from datetime import datetime, timedelta
from googletrans import Translator

import pytz
import os
import time


# Scroll to the bottom of the page to load older content for older post
def scroll_to_load(driver, max_scrolls=8):
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


# Set up the WebDriver for Firefox
service = Service("geckodriver.exe")  # Update this path to where your geckodriver is located
driver = webdriver.Firefox(service=service)
post_links = {}

try:
    # Open the Bilibili page
    url = "https://space.bilibili.com/57276677/dynamic"
    driver.get(url)

    # Wait for the page to load
    driver.implicitly_wait(10)

    # COMMENT when automation
    # scroll_to_load(driver, max_scrolls=6)

    posts = driver.find_elements(By.CLASS_NAME, "bili-dyn-item")  # Fetch all posts
    try:
        local_date = datetime.now()
        for post in posts:
            # Dynamic Date
            current_year = datetime.now().year
            dynamic_date_card = post.find_element(By.CLASS_NAME, "bili-dyn-item__desc")
            dynamic_date = str(dynamic_date_card.text)
            dynamic_type = str(dynamic_date_card.text.split()[-1]) # jump video
            if dynamic_type[-2:] != "文章":
                continue

            # Dynamic ID
            dynamic_id_card = post.find_element(By.CLASS_NAME, "dyn-card-opus")
            dynamic_id = dynamic_id_card.get_attribute("dyn-id")

            # Dynamic Title
            dynamic_title = dynamic_id_card.text
            title_short = str(dynamic_title)[:15]

            # Check for the desired post title
            if "《日·键圈时刻表》" in title_short or "键圈时刻表" in title_short:
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
                    else: # M-D

                        local_date = datetime.strptime(date_list[0], "%m月%d日").strftime("%m-%d")
                        local_date = str(current_year) + '-' + local_date
                '''DATE CHECK'''
                if local_date[:4] != str(current_year):
                    break
                # title
                translator = Translator()
                title_content = dynamic_title.split("》")[1]
                title_content = title_content.split("\n")[0]
                translated_content = translator.translate(title_content, src="zh-CN", dest="en")
                # image
                download_images(post, local_date)
                # link
                post_links[local_date] = [f"https://www.bilibili.com/opus/{dynamic_id}", translated_content.text]
                print(f"Found: {local_date}")
                break
        file_path = "dynamics.txt"
        if local_date not in post_links:
            print("Date Post Error")
        append_most_recent_post(file_path, local_date, post_links[local_date][0], post_links[local_date][1])
    except Exception as e:
        print(f"Error processing post: {e}")

except Exception as e:
    print(f"Webpage Open Failed: {e}")

finally:
    # Close the browser
    driver.quit()
