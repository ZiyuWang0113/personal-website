from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from datetime import datetime, timedelta
import pytz

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

    posts = driver.find_elements(By.CLASS_NAME, "bili-dyn-item")  # Fetch all posts
    for post in posts:
        try:
            # Dynamic Date
            dynamic_date_card = post.find_element(By.CLASS_NAME, "bili-dyn-item__desc")
            dynamic_date = str(dynamic_date_card.text)

            # Dynamic ID
            dynamic_id_card = post.find_element(By.CLASS_NAME, "dyn-card-opus")
            dynamic_id = dynamic_id_card.get_attribute("dyn-id")

            # Dynamic Title
            dynamic_title = dynamic_id_card.text
            title_short = str(dynamic_title)[:15]

            # Check for the desired post title
            if "《日·键圈时刻表》" in title_short or "键圈时刻表" in title_short:
                date_list = dynamic_date.split(' ')
                if date_list[0] == "昨天" or date_list[0] == "前天":
                    cur_time = datetime.now()
                    localFormat = "%Y-%m-%d"
                    tz = 'Asia/Shanghai'
                    localDatetime = cur_time.astimezone(pytz.timezone(tz))
                    delta = 1 if date_list[0] == "昨天" else 2
                    local_date = localDatetime - timedelta(days=delta)
                    local_date = local_date.strftime(localFormat)
                else:
                    local_date = datetime.strptime(date_list[0], "%m月%d日").strftime("%Y-%m-%d")

                post_links[local_date] = f"https://www.bilibili.com/opus/{dynamic_id}"
                print(f"Found: {local_date} -> {post_links[local_date]}")
                break
        except Exception as e:
            print(f"Error processing post: {e}")
            continue

    # Write to a file
    file_path = "post_links.txt"
    with open(file_path, "a+", encoding="utf-8") as file:
        file.seek(0)
        existing_data = file.read()
        for date, link in post_links.items():
            if date not in existing_data:
                file.write(f"{date}: {link}\n")
                print(f"Appended: {date}: {link}")

except Exception as e:
    print(f"Webpage Open Failed: {e}")
finally:
    # Close the browser
    driver.quit()
