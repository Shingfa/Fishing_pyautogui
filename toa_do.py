import pyautogui
import time

print("Di chuột đến vị trí cần lấy. Nhấn Ctrl + C trong Terminal để dừng.")
try:
    while True:
        x, y = pyautogui.position()
        color = pyautogui.pixel(x, y)
        print(f"Toạ độ: X={x:4d}, Y={y:4d} | Màu RGB: {color}", end="\r")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nĐã dừng.")