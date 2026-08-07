import pyautogui
import time

# ================= CẤU HÌNH TỌA ĐỘ, VÙNG & MÀU SẮC =================
WATER_POS = (507, 523)  
SEARCH_REGION = (356, 373, 300, 300) 
FLOAT_RED_COLOR = (207, 29, 45) 
COLOR_TOLERANCE = 50               

DISCARD_POS = (662, 668) 
DISCARD_COLOR = (0, 48, 62) 

SUBMERGE_TIME = 0.2
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
    return pyautogui.pixelMatchesColor(DISCARD_POS[0], DISCARD_POS[1], DISCARD_COLOR, tolerance=30)

print("Bắt đầu Auto sau 3 giây...")
time.sleep(3)

try:
    while True:
        print("Quăng cần...")
        pyautogui.click(WATER_POS)
        time.sleep(3.0) 
        
        print("Đang khóa mục tiêu phao trong vùng quét...")
        phat_hien_phao = False
        for _ in range(50): 
            if is_color_in_region(SEARCH_REGION, FLOAT_RED_COLOR, COLOR_TOLERANCE):
                phat_hien_phao = True
                break
            time.sleep(0.1)
            
        if not phat_hien_phao:
            print("Lỗi: Không thấy phao đỏ trong vùng quét. Bắt đầu lại...")
            continue
            
        print("Đã thấy phao. Đang đợi cá cắn...")
        ca_can = False
        start_wait = time.time()
        disappear_start = None 
        
        while time.time() - start_wait < 40: 
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
            print("Chờ quá lâu không thấy cá cắn. Quăng lại...")
            pyautogui.click(WATER_POS) 
            time.sleep(2.0)
            continue
            
        pyautogui.mouseDown(WATER_POS[0], WATER_POS[1]) 
        
        print("Đang kéo cần, chờ nút Bỏ cá xuất hiện (mất khoảng 5 giây)...")
        # Nghỉ ngơi 4 giây đầu tiên, không cần quét màn hình để tiết kiệm tài nguyên
        time.sleep(5.95) 
        
        wait_pull = time.time()
        while True:
            if check_discard_button():
                print("Thả cá...")
                break
            
            # Tăng thời gian chờ an toàn lên 15 giây phòng trường hợp giật lag
            if time.time() - wait_pull > 15: 
                print("Lỗi kéo cần (tuột cá). Bắt đầu lại...")
                break
            time.sleep(0.1)
            
        pyautogui.mouseUp(WATER_POS[0], WATER_POS[1])
        time.sleep(0.5) 
        pyautogui.click(DISCARD_POS)
        time.sleep(1.8) 

except KeyboardInterrupt:
    pyautogui.mouseUp() 
    print("\nĐã dừng chương trình Auto.")