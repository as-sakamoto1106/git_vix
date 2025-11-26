import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def download_vix_chart():
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # Bot対策（普通のブラウザに見せる）
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    print("Launching Chrome...")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        driver.get(url)

        # グラフが表示されるまで待つ
        # ここで "highcharts-container" を探すのは成功している
        chart_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Chart loaded.")

        # アニメーション待ち（線が伸び切るのを待つ）
        time.sleep(5)

        # 念のためポップアップ消し
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass

        target_file = "vix_chart.png"
        
        # ▼▼▼ 修正箇所：IDではなく、さっき見つけた element をそのまま使う ▼▼▼
        # 画面のトップ位置へスクロールして調整（確実に映すため）
        driver.execute_script("arguments[0].scrollIntoView();", chart_element)
        time.sleep(1)
        
        # その要素だけをパシャリと撮る
        chart_element.screenshot(target_file)
        # ▲▲▲ 修正ここまで ▲▲▲

        print(f"Success! Screenshot saved as {target_file}")
        
        if os.path.exists(target_file):
            print(f"File size: {os.path.getsize(target_file)} bytes")
        else:
            raise Exception("File was not saved.")

    except Exception as e:
        print(f"Error: {e}")
        # エラー時は画面全体を撮って、Artifactsで見れるようにする
        driver.save_screenshot("debug_error.png")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    download_vix_chart()