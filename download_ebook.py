import os
import requests
from PIL import Image
from io import BytesIO

# 瀏覽器偽裝，避免被伺服器阻擋
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://digitaiyucoo.com/"
}

def main():
    print("="*50)
    print("泰宇行動備課快遞 電子書下載轉 PDF 工具 ")
    print("="*50)

    # 1. 讓使用者輸入網址
    user_url = input("🔗 請貼上你要下載的電子書網址 (例如 https://.../mobile/index.html)：\n> ").strip()
    if not user_url:
        print("...? 網址不能為空！")
        return

    # 2. 讓使用者輸入想儲存的 PDF 檔名
    output_pdf = input("請為這本書取個檔名 (例如 CH4_講義.pdf)：\n> ").strip()
    # 設置防呆機制：如果沒輸入檔名，給個預設值；如果沒打 .pdf 附檔名，自動補上
    if not output_pdf:
        output_pdf = "ebook_download.pdf"
    elif not output_pdf.lower().endswith('.pdf'):
        output_pdf += '.pdf'

    # 3. 讓使用者指定儲存路徑
    output_dir = input("📂 請輸入要儲存的資料夾路徑 (直接按 Enter 代表存放在當前資料夾)：\n> ").strip()
    
    if output_dir:
        # 如果使用者輸入了路徑，就確保該資料夾存在 (不存在會自動建立)
        os.makedirs(output_dir, exist_ok=True)
        # 將路徑和檔名安全地結合起來
        final_output_path = os.path.join(output_dir, output_pdf)
    else:
        # 如果留空，就直接存當前目錄
        final_output_path = output_pdf
        
    # 4. 處理字串：取得基礎目錄
    base_url = user_url.split('/mobile')[0].split('/index.html')[0]
    if not base_url.endswith('/'):
        base_url += '/'

    page = 1
    image_list = []

    print(f"\n準備就緒，目標書本路徑：{base_url}")
    print(f"預計儲存位置：{os.path.abspath(final_output_path)}")
    print("開始下載並轉換電子書 (不產生暫存圖檔)...")

    while True:
        url_large = f"{base_url}files/large/{page}.jpg"
        url_mobile = f"{base_url}files/mobile/{page}.jpg"
        
        response = requests.get(url_large, headers=HEADERS)
        
        if response.status_code != 200:
            response = requests.get(url_mobile, headers=HEADERS)

        if response.status_code == 200:
            try:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                image_list.append(img)
                print(f"第 {page} 頁下載並處理成功！")
            except Exception as e:
                print(f"⚠️ 處理第 {page} 頁時發生錯誤: {e}")
            
            page += 1
        else:
            print(f"已到達最後一頁。總共下載了 {page - 1} 頁。")
            break

    if image_list:
        print(f"⏳ 正在將內容合併並儲存為 PDF ...")
        image_list[0].save(
            final_output_path, 
            save_all=True, 
            append_images=image_list[1:]
        )
        print(f"🎉 任務完成！你的檔案已經成功儲存在：\n👉 {os.path.abspath(final_output_path)}")
    else:
        print("❌ 沒有下載到任何內容，請檢查網址是否正確或伺服器是否正常。")

if __name__ == "__main__":
    main()