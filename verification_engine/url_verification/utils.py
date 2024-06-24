import time
import requests
from io import BytesIO
from PIL import Image
import imagehash
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def download_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

def calculate_similarity(image1, image2):
    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)
    return 1 - (hash1 - hash2) / len(hash1.hash) ** 2

def google_lens(img_url, driver, wait):
    driver.get(f'https://lens.google.com/uploadbyurl?url={img_url}')
    wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, 'wETe9b jFVN1')]")))
    related_images = driver.find_elements(By.XPATH, "//img[contains(@class, 'wETe9b jFVN1')]")
    
    related_image_urls = []
    for image in related_images:
        if image.get_attribute('src').startswith('https://'):
            related_image_urls.append(image.get_attribute('src'))
    return related_image_urls

def naver(img_url, driver, wait):
    driver.get(f'https://s.search.naver.com/p/sbi/search.naver?where=sbi&query=smartlens&orgPath={img_url}')
    wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@alt, '이미지준비중')]")))
    related_images = driver.find_elements(By.XPATH, "//img[contains(@alt, '이미지준비중')]")

    related_image_urls = []
    for image in related_images:
        if image.get_attribute('src').startswith('https://'):
            url = image.get_attribute('src').split('&')[0]
            related_image_urls.append(url)
    return related_image_urls

def yandex(img_url, driver, wait):
    driver.get(f'https://yandex.com/images/search?rpt=imageview&url={img_url}')
    similar_btn = driver.find_element(By.XPATH,"//a[contains(@class, 'CbirNavigation-TabsItem CbirNavigation-TabsItem_name_similar-page')]")
    similar_btn.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, 'serp-item__thumb justifier__thumb')]")))
    related_images = driver.find_elements(By.XPATH,"//img[contains(@class, 'serp-item__thumb justifier__thumb')]")

    related_image_urls = []
    for image in related_images:
        if image.get_attribute('src').startswith('https://'):
            related_image_urls.append(image.get_attribute('src'))
    return related_image_urls

def search_similar_images(img_url):
    driver, wait = initialize_driver()
    original_image = download_image(img_url)
    
    results = {
        'Google:': [],
        'Naver:': [],
        'Yandex:': []
    }
    
    google_images = google_lens(img_url, driver, wait)
    naver_images = naver(img_url, driver, wait)
    yandex_images = yandex(img_url, driver, wait)
    
    for img in google_images:
        try:
            similar_image = download_image(img)
            similarity = calculate_similarity(original_image, similar_image) * 100  # Convert to percentage
            results['Google:'].append({'url': img, 'similarity': similarity})
        except Exception as e:
            results['Google:'].append({'url': img, 'similarity': f"Error: {str(e)}"})
    
    for img in naver_images:
        try:
            similar_image = download_image(img)
            similarity = calculate_similarity(original_image, similar_image) * 100  # Convert to percentage
            results['Naver:'].append({'url': img, 'similarity': similarity})
        except Exception as e:
            results['Naver:'].append({'url': img, 'similarity': f"Error: {str(e)}"})
    
    for img in yandex_images:
        try:
            similar_image = download_image(img)
            similarity = calculate_similarity(original_image, similar_image) * 100  # Convert to percentage
            results['Yandex:'].append({'url': img, 'similarity': similarity})
        except Exception as e:
            results['Yandex:'].append({'url': img, 'similarity': f"Error: {str(e)}"})
    
    driver.quit()
    
    # Sort results by similarity in descending order
    for key in results:
        results[key] = sorted(results[key], key=lambda x: x['similarity'], reverse=True)
    
    return results

# Example usage
# if __name__ == "__main__":
#     img_url = "https://live.staticflickr.com/4737/27802760289_0611c27865_z.jpg"
#     similar_images = search_similar_images(img_url)
#     print(similar_images)
