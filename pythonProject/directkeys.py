import ctypes
import time

SendInput = ctypes.windll.user32.SendInput
# 需要禁用小键盘
up = 0x48
down = 0x50
left = 0x4b
right = 0x4d

A = 0x1E
S = 0x1F
D = 0x20
F = 0x21
G = 0x22
space = 0x39
f1 = 0x3B
f2 = 0x3C
f3 = 0x3D
f4 = 0x3E
f5 = 0x3F
f6 = 0x40
tab = 0x0F
enter = 0x1C

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# action_num = 10
# 俯冲
def dive(t):
    PressKey(up)
    time.sleep(t)
    ReleaseKey(up)

# 爬升
def climb(t):
    PressKey(down)
    time.sleep(t)
    ReleaseKey(down)

# 左横滚转向
def turnleft(t):
    PressKey(left)
    time.sleep(t)
    ReleaseKey(left)

# 右横滚转向
def turnright(t):
    PressKey(right)
    time.sleep(t)
    ReleaseKey(right)

# 加速
def speedup(t):
    PressKey(A)
    time.sleep(t)
    ReleaseKey(A)

# 减速
def speeddown(t):
    PressKey(S)
    time.sleep(t)
    ReleaseKey(S)

# 切换NTS目标
def switchNTS_T():
    PressKey(D)
    time.sleep(0.05)
    ReleaseKey(D)

# 切换NTS成员
def switchNTS_M():
    PressKey(F)
    time.sleep(0.05)
    ReleaseKey(F)

# 切换NTS武器
def switchNTS_W():
    PressKey(G)
    time.sleep(0.05)
    ReleaseKey(G)

# 发射导弹
def launch_W():
    PressKey(space)
    time.sleep(0.05)
    ReleaseKey(space)

# 测试
if __name__ == '__main__':
    time.sleep(2)
    time1 = time.time()
    while (True):
        if abs(time.time() - time1) > 45: # 超时退出
            break
        else:
            dive(2)
            climb(2)
            turnleft(2)
            turnright(2)
            speedup(2)
            speeddown(2)
            switchNTS_T()
            switchNTS_M()
            switchNTS_W()

# wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
