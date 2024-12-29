from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

app = Flask(__name__)
CORS(app)

PROXY_URL = os.getenv('PROXY_URL')

def scrape_trends():
    driver = None
    try:
        if not PROXY_URL:
            raise ValueError("Proxy URL is missing or invalid in the environment variables.")
        
        chrome_options = Options()
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = PROXY_URL
        proxy.ssl_proxy = PROXY_URL
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--proxy-server=%s' % PROXY_URL)
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get("https://x.com/home")
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Timeline: Trending now"]')))
        
        time.sleep(2)

        trend_elements = driver.find_elements(By.XPATH, '//div[@aria-label="Timeline: Trending now"]//div[@data-testid="trend"]')
        trends = [trend.text for trend in trend_elements if trend.text]

        if not trends:
            raise ValueError("No trending topics found. The XPath might be incorrect or the page structure may have changed.")
        
        return trends[:5]

    except Exception as e:
        print(f"Error while scraping: {e}")
        return []
    finally:
        if driver:
            driver.quit()

@app.route('/run-scraping', methods=['GET'])
def run_scraping():
    try:
        if not PROXY_URL:
            return jsonify({"error": "Proxy URL is missing or invalid in the environment variables."}), 400

        trends = scrape_trends()
        
        if PROXY_URL:
            ip_address = PROXY_URL.split('@')[-1].split(':')[0]
        else:
            ip_address = "Unknown"
        
        return jsonify({
            "trends": trends if trends else ["No trends found"],
            "ip_address": ip_address
        })
    except Exception as e:
        print(f"Error in run_scraping: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)