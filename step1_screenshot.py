import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def run_screenshot():
    print("=== STEP 1: Screenshot Start ===")
    
    # ブラウザ設定
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    target_file = "vix_chart.png"

    try:
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        driver.get(url)

        # グラフ待ち
        chart_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Chart loaded.")
        
        # アニメーション待ち
        time.sleep(5)
        
        # ポップアップ消し
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass

        # 撮影
        driver.execute_script("arguments[0].scrollIntoView();", chart_element)
        time.sleep(1)
        chart_element.screenshot(target_file)
        print(f"Screenshot saved: {target_file}")

    except Exception as e:
        print(f"Step 1 Error: {e}")
        driver.save_screenshot("debug_error.png")
        exit(1)
    finally:
        driver.quit()
        print("=== STEP 1: Finished ===")

if __name__ == "__main__":
    run_screenshot()