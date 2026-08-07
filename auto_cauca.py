import pyautogui
import time
#day 28/7
# ================= CẤU HÌNH TỌA ĐỘ, VÙNG & MÀU SẮC =================
WATER_POS = (466, 595)  
SEARCH_REGION = (316, 445, 250, 250) 
FLOAT_RED_COLOR = (213, 17, 36) 
COLOR_TOLERANCE = 50               

DISCARD_POS = (662, 668) 
DISCARD_COLOR = (0, 48, 62) 

SUBMERGE_TIME = 0.15
MAX_WAIT_BITE = 30
# ===================================================================

def is_color_in_region(region, target_color, tolerance=30):
    img = pyautogui.screenshot(region=region)
    width, height = img.size
    for x in range(0, width, 5):
        for y in range(0, height, 5):
            r, g, b = img.getpixel((x, y))
            if (abs(r - target_color[0]) <= tolerance and 
                abs(g - target_color[1]) <= tolerance and 
                abs(b - target_color[2]) <= tolerance):
                return True
    return False

def check_discard_button():
    # SỬA LỖI 2: Hạ tolerance xuống 5 để không bao giờ nhận diện nhầm mặt nước đen thành nút Bỏ cá
    return pyautogui.pixelMatchesColor(DISCARD_POS[0], DISCARD_POS[1], DISCARD_COLOR, tolerance=5)

print("Bắt đầu Auto sau 3 giây...")
time.sleep(3)

try:
    while True:
        print("\n--- BẮT ĐẦU LƯỢT MỚI ---")
        
        # --- KHỐI 1: VÒNG LẶP QUĂNG CẦN THÔNG MINH (CHỐNG LỆCH NHỊP) ---
        phat_hien_phao = False
        while not phat_hien_phao:
            print("Quăng cần...")
            pyautogui.click(WATER_POS)
            time.sleep(3.0) 
            
            print("Đang khóa mục tiêu phao...")
            for _ in range(50): 
                if is_color_in_region(SEARCH_REGION, FLOAT_RED_COLOR, COLOR_TOLERANCE):
                    phat_hien_phao = True
                    break
                time.sleep(0.1)
            
            if not phat_hien_phao:
                print("Lỗi: Quăng xịt hoặc lệch nhịp. Đang tự động nắn lại nhịp...")
                if check_discard_button():
                    pyautogui.click(DISCARD_POS)
                    time.sleep(2.0)
                else:
                    # Nghỉ 2s trước khi vòng lặp tự động quay lại click WATER_POS để nắn nhịp
                    time.sleep(2.0) 
        
        # --- KHỐI 2: CHỜ CÁ CẮN ---
        print("Đã thấy phao. Đang đợi cá cắn...")
        ca_can = False
        start_wait = time.time()
        disappear_start = None 
        
        while time.time() - start_wait < MAX_WAIT_BITE: 
            phao_con_noi = is_color_in_region(SEARCH_REGION, FLOAT_RED_COLOR, COLOR_TOLERANCE)
            
            if not phao_con_noi:
                if disappear_start is None:
                    disappear_start = time.time()
                elif time.time() - disappear_start >= SUBMERGE_TIME:
                    print("Cá cắn thật (chìm hẳn)! Bắt đầu kéo...")
                    ca_can = True
                    break
            else:
                disappear_start = None
                
            time.sleep(0.05) 
            
        if not ca_can:
            print("Chờ quá lâu không có cá. Chủ động thu cần...")
            pyautogui.click(WATER_POS) 
            time.sleep(3.0)
            continue 
            
        # --- KHỐI 3: KÉO CÁ & THẢ CÁ ---
        # SỬA LỖI 1: Thay mouseDown (nhấn giữ) thành click 1 lần theo đúng cơ chế game
        print("Giật cần! (Click 1 lần)...")
        pyautogui.click(WATER_POS) 
        
        print("Đang chờ nhân vật kéo cá lên...")
        time.sleep(5.95) 
        
        wait_pull = time.time()
        keo_thanh_cong = False
        
        while True:
            if check_discard_button():
                keo_thanh_cong = True
                break
            
            if time.time() - wait_pull > 15: 
                break
            time.sleep(0.1)
            
        if keo_thanh_cong:
            print("Thả cá...")
            pyautogui.click(DISCARD_POS)
            time.sleep(1.8) 
        else:
            print("Lỗi kéo cần (tuột cá). Chuẩn bị quăng lại...")
            time.sleep(1.8)

except KeyboardInterrupt:
    print("\nĐã dừng chương trình Auto.")