import pyautogui
import time

def send_message(base_message, count):
    for i in range(1, count + 1): 
        message_with_counter = f"{base_message} {i}" 
        pyautogui.typewrite(message_with_counter)
        pyautogui.press("enter")

if __name__ == "__main__":
    time.sleep(5)  
    send_message(" ", 1000)
