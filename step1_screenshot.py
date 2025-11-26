import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def run_screenshot():
    print("=== STEP 1: Screenshot Start ===")
    
    options = Options()
    # ヘッドレス設定
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    
    # ▼▼▼ 重要：サーバーでのクラッシュを防ぐ追加オプション ▼▼▼
    options.add_argument("--disable-dev-shm-usage") # メモリ不足対策
    options.add_argument("--disable-gpu")           # GPU無効化
    options.add_argument("--remote-debugging-port=9222") # ポート固定
    options.add_argument("--window-size=1920,1080")
    
    # User-Agent偽装
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    # ▼▼▼ 最重要：読み込み完了を待たずに次へ進む設定（エラー回避） ▼▼▼
    options.set_capability("pageLoadStrategy", "eager")

    print("Launching Chrome with Eager Strategy...")
    driver = webdriver.Chrome(options=options)
    
    # 読み込みタイムアウトを短めに設定（万が一のために）
    driver.set_page_load_timeout(30)
    
    wait = WebDriverWait(driver, 20)
    target_file = "vix_chart.png"

    try:
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        
        try:
            driver.get(url)
        except Exception as e:
            # Eagerモードでもタイムアウトすることがあるが、
            # 画面が出ていればOKなので、ここではエラーを無視して進む
            print(f"Warning during loading (ignoring): {e}")

        # グラフが表示されるのを「明示的に」待つ
        print("Waiting for chart element...")
        chart_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Chart loaded detected.")
        
        # 描画待ち
        time.sleep(5)
        
        # ポップアップ消し
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass

        # 撮影
        print("Taking screenshot...")
        driver.execute_script("arguments[0].scrollIntoView();", chart_element)
        time.sleep(1)
        chart_element.screenshot(target_file)
        
        if os.path.exists(target_file):
            print(f"Screenshot saved successfully: {target_file}")
            print(f"File size: {os.path.getsize(target_file)} bytes")
        else:
            raise Exception("File was not saved.")

    except Exception as e:
        print(f"Step 1 Error: {e}")
        # デバッグ用画像の保存（失敗時のみ）
        try:
            driver.save_screenshot("debug_error.png")
        except:
            pass
        exit(1)
    finally:
        driver.quit()
        print("=== STEP 1: Finished ===")

if __name__ == "__main__":
    run_screenshot()