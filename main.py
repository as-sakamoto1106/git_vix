import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def download_vix_chart():
    # 設定
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
        # vixcentralは "highcharts-container" というクラスの中にグラフがある
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Chart loaded.")

        # 重要：グラフのアニメーション（線がニョキニョキ伸びる動き）が終わるまで少し待つ
        time.sleep(5)

        # 念のため、余計なポップアップなどを消すためにbodyをクリックしておく（任意）
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass

        # ▼▼▼ ダウンロードではなく、グラフ要素を直接撮影する ▼▼▼
        target_file = "vix_chart.png"
        
        # グラフの要素（div）を特定して、そこだけスクショをとる
        # VIX Centralの構造上、メインのグラフは id="home_container" または class="highcharts-container"
        chart_element = driver.find_element(By.ID, "home_container")
        
        # 保存
        chart_element.screenshot(target_file)
        print(f"Success! Screenshot saved as {target_file}")
        
        # ファイルが本当にできたか確認
        if os.path.exists(target_file):
            print(f"File size: {os.path.getsize(target_file)} bytes")
        else:
            raise Exception("File was not saved.")

    except Exception as e:
        print(f"Error: {e}")
        # エラー時は画面全体を撮ってデバッグ用に残す
        driver.save_screenshot("debug_error.png")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    download_vix_chart()