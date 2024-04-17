import keyboard

def on_key_event(event):
    print("Key:", event.name)
    print("Scan Code:", event.scan_code)

keyboard.hook(on_key_event)
keyboard.wait('esc')  # 等待按下Esc键来退出程序