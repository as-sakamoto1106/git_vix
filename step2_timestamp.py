import os
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

def run_timestamp():
    print("=== STEP 2: Timestamp Start ===")
    target_file = "vix_chart.png"

    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found. Step 1 failed?")
        exit(1)

    try:
        # 日本時間の計算
        jst_now = datetime.utcnow() + timedelta(hours=9)
        date_str = jst_now.strftime("%Y-%m-%d %H:%M JST")
        
        # 画像を開く
        img = Image.open(target_file)
        draw = ImageDraw.Draw(img)
        
        # デフォルトフォントを使用（エラー回避のため）
        # ※サーバー上だとデフォルトはかなり小さいですが、まずは動くことを優先します
        font = ImageFont.load_default()

        # 文字が見やすいように背景に白い四角を描く
        # (左上x, 左上y, 右下x, 右下y)
        draw.rectangle((5, 5, 160, 25), fill="white")
        
        # 文字を描く (座標, 文字列, 色, フォント)
        draw.text((10, 10), date_str, fill="red", font=font)
        
        # 上書き保存
        img.save(target_file)
        print(f"Timestamp added: {date_str}")

    except Exception as e:
        print(f"Step 2 Error: {e}")
        exit(1)
    
    print("=== STEP 2: Finished ===")

if __name__ == "__main__":
    run_timestamp()