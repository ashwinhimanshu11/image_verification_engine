import asyncio
import aiohttp
from aiohttp import ClientSession
from PIL import Image
from io import BytesIO
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)  # Increased wait time
    return driver, wait

async def download_image(image_url, session: ClientSession):
    async with session.get(image_url) as response:
        content = await response.read()
        img = Image.open(BytesIO(content)).convert('RGB')
        return img

def calculate_histogram_similarity(image1, image2):
    # Calculate histograms for each channel
    hist1 = image1.histogram()
    hist2 = image2.histogram()
    
    # Normalize the histograms
    hist1 = np.array(hist1) / sum(hist1)
    hist2 = np.array(hist2) / sum(hist2)
    
    # Calculate the similarity percentage
    similarity = np.sum(np.minimum(hist1, hist2)) * 100
    
    return similarity

async def google_lens(img_url, driver, wait):
    try:
        start_time = time.time()
        driver.get(f'https://lens.google.com/uploadbyurl?url={img_url}')
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, 'wETe9b jFVN1')]")))
        related_images = driver.find_elements(By.XPATH, "//img[contains(@class, 'wETe9b jFVN1')]")
        
        related_image_urls = []
        for image in related_images:
            if image.get_attribute('src').startswith('https://'):
                related_image_urls.append({
                    'url': image.get_attribute('src'),
                    'source': f"https://lens.google.com/uploadbyurl?url={image.get_attribute('src')}"
                })
        end_time = time.time()
        print(f"Google Lens found {len(related_image_urls)} images in {end_time - start_time} seconds")
        return related_image_urls[:10]  # Limit results
    except Exception as e:
        print(f"Google Lens error: {e}")
        return []

async def naver(img_url, driver, wait):
    try:
        start_time = time.time()
        driver.get(f'https://s.search.naver.com/p/sbi/search.naver?where=sbi&query=smartlens&orgPath={img_url}')
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@alt, '이미지준비중')]")))
        related_images = driver.find_elements(By.XPATH, "//img[contains(@alt, '이미지준비중')]")

        related_image_urls = []
        for image in related_images:
            if image.get_attribute('src').startswith('https://'):
                url = image.get_attribute('src').split('&')[0]
                related_image_urls.append({
                    'url': url,
                    'source': f"https://s.search.naver.com/p/sbi/search.naver?where=sbi&query=smartlens&orgPath={url}"
                })
        end_time = time.time()
        print(f"Naver found {len(related_image_urls)} images in {end_time - start_time} seconds")
        return related_image_urls[:10]  # Limit results
    except Exception as e:
        print(f"Naver error: {e}")
        return []

async def yandex(img_url, driver, wait):
    try:
        start_time = time.time()
        driver.get(f'https://yandex.com/images/search?rpt=imageview&url={img_url}')
        similar_btn = driver.find_element(By.XPATH, "//a[contains(@class, 'CbirNavigation-TabsItem CbirNavigation-TabsItem_name_similar-page')]")
        similar_btn.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, 'serp-item__thumb justifier__thumb')]")))
        related_images = driver.find_elements(By.XPATH, "//img[contains(@class, 'serp-item__thumb justifier__thumb')]")

        related_image_urls = []
        for image in related_images:
            if image.get_attribute('src').startswith('https://'):
                related_image_urls.append({
                    'url': image.get_attribute('src'),
                    'source': f"https://yandex.com/images/search?rpt=imageview&url={image.get_attribute('src')}"
                })
        end_time = time.time()
        print(f"Yandex found {len(related_image_urls)} images in {end_time - start_time} seconds")
        return related_image_urls[:10]  # Limit results
    except Exception as e:
        print(f"Yandex error: {e}")
        return []

async def bing(img_url, driver, wait):
    try:
        start_time = time.time()
        driver.get(f'https://www.bing.com/images/searchbyimage?cbir=ssbi&imgurl={img_url}')
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@alt, 'See related image detail.')]")))
        related_images = driver.find_elements(By.XPATH, "//img[contains(@alt, 'See related image detail.')]")
        
        related_image_urls = []
        for image in related_images:
            if image.get_attribute('src').startswith('https://'):
                related_image_urls.append({
                    'url': image.get_attribute('src'),
                    'source': f"https://www.bing.com/images/searchbyimage?cbir=ssbi&imgurl={image.get_attribute('src')}"
                })
        end_time = time.time()
        print(f"Bing found {len(related_image_urls)} images in {end_time - start_time} seconds")
        return related_image_urls[:10]  # Limit results
    except Exception as e:
        print(f"Bing error: {e}")
        return []

async def search_similar_images(img_url):
    driver, wait = initialize_driver()
    async with ClientSession() as session:
        start_time = time.time()
        original_image = await download_image(img_url, session)
        
        results = {
            'Google:': [],
            'Naver:': [],
            'Yandex:': [],
            'Bing:': []
        }
        
        google_images_task = asyncio.create_task(google_lens(img_url, driver, wait))
        naver_images_task = asyncio.create_task(naver(img_url, driver, wait))
        yandex_images_task = asyncio.create_task(yandex(img_url, driver, wait))
        bing_images_task = asyncio.create_task(bing(img_url, driver, wait))
        
        google_images = await google_images_task
        naver_images = await naver_images_task
        yandex_images = await yandex_images_task
        bing_images = await bing_images_task
        
        image_tasks = []
        for img in google_images:
            image_tasks.append((img['url'], download_image(img['url'], session), 'Google:', img['source']))
        
        for img in naver_images:
            image_tasks.append((img['url'], download_image(img['url'], session), 'Naver:', img['source']))
        
        for img in yandex_images:
            image_tasks.append((img['url'], download_image(img['url'], session), 'Yandex:', img['source']))
        
        for img in bing_images:
            image_tasks.append((img['url'], download_image(img['url'], session), 'Bing:', img['source']))
        
        download_start_time = time.time()
        downloaded_images = await asyncio.gather(*[task[1] for task in image_tasks])
        download_end_time = time.time()
        print(f"Downloaded all images in {download_end_time - download_start_time} seconds")

        for idx, (img_url, _, engine, source_url) in enumerate(image_tasks):
            try:
                similar_image = downloaded_images[idx]
                similarity = calculate_histogram_similarity(original_image, similar_image)  # Histogram similarity
                results[engine].append({'url': img_url, 'similarity': f'{similarity:.3f}', 'source': source_url})
            except Exception as e:
                results[engine].append({'url': img_url, 'similarity': f"Error: {str(e)}", 'source': source_url})
        
        # Sort results by similarity in descending order
        for key in results:
            results[key] = sorted(results[key], key=lambda x: x['similarity'], reverse=True)
        
        driver.quit()
        end_time = time.time()
        print(f"Total time for search_similar_images: {end_time - start_time} seconds")
        return results

# Example usage
# if __name__ == "__main__":
#     img_url = "https://live.staticflickr.com/4737/27802760289_0611c27865_z.jpg"
#     similar_images = asyncio.run(search_similar_images(img_url))
#     print(similar_images)
