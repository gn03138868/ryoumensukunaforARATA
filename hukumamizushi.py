#hukumamizushi (伏魔御廚子)
#ryoumensukunaforARATA folder version
#ryukoku hinoki segmented image data


from PIL import Image
import os

# 請修改以下路徑為實際的輸入/輸出資料夾
input_folder = r"Z:\RF for bamboo\Root for Hirano sensei and Ohashi sensei\Ryukoku\segmented image data"   # 存放 JPEG 圖片的資料夾
output_folder = r"Z:\RF for bamboo\Root for Hirano sensei and Ohashi sensei\Ryukoku\cut segmented image data"   # 輸出切割後圖片的資料夾

# crop size 定義
crop_size = (400, 400)

def crop_image(image_path, output_folder, crop_size):
    # 開啟圖片檔案
    with Image.open(image_path) as img:
        img = img.convert('RGB')  # 轉換成 RGB 模式
        original_dpi = img.info.get('dpi', (600, 600))  # 若無 dpi 資訊，預設為 600 dpi
        print(f"處理 {os.path.basename(image_path)}，原始 DPI: {original_dpi}")
        
        # 取得圖片寬度和高度
        img_width, img_height = img.size
        if isinstance(crop_size, int):
            crop_width = crop_height = crop_size
        elif isinstance(crop_size, tuple) and len(crop_size) == 2:
            crop_width, crop_height = crop_size
        else:
            raise ValueError("crop_size 應為 int 或含兩個 int 的 tuple")
        
        # 計算水平方向與垂直方向可以切割幾塊
        crops_w = img_width // crop_width
        crops_h = img_height // crop_height
        count = 0
        for i in range(crops_h):
            for j in range(crops_w):
                left = j * crop_width
                top = i * crop_height
                right = left + crop_width
                bottom = top + crop_height
                
                # 切割圖片
                cropped_img = img.crop((left, top, right, bottom))
                # 組合輸出檔名
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(output_folder, f"{base_name}_{left}_{top}_{right}_{bottom}_{count}_arata.jpg")
                # 儲存切割後圖片，保留原 DPI 與品質
                cropped_img.save(output_path, 'JPEG', dpi=original_dpi, quality=100)
                
                # 驗證儲存後圖片的 DPI
                with Image.open(output_path) as saved_img:
                    saved_dpi = saved_img.info.get('dpi', (0, 0))
                    print(f"儲存圖片 {os.path.basename(output_path)} 的 DPI: {saved_dpi}")
                    if saved_dpi != original_dpi:
                        print(f"警告: {output_path} 的 DPI 不一致")
                
                count += 1

def process_folder(input_folder, output_folder, crop_size):
    os.makedirs(output_folder, exist_ok=True)  # 確保輸出資料夾存在
    # 遍歷輸入資料夾中所有檔案（僅處理 .jpg 與 .jpeg）
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                crop_image(image_path, output_folder, crop_size)

# 執行處理
process_folder(input_folder, output_folder, crop_size)
