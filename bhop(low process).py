import keyboard
import pymem
import pymem.process
import time
from win32gui import GetWindowText, GetForegroundWindow
import requests

#dwForceJump = (0x51FBFA8)
#dwLocalPlayer = (0xD3DD14)
#m_fFlags = (0x104)

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwForceJump = int(response["signatures"]["dwForceJump"])

m_fFlags = int(response["netvars"]["m_fFlags"])


def main():
    print("BHOP TEST LAUNCH")
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    player = pm.read_int(client + dwLocalPlayer)

    while True:
        if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
            continue
        if keyboard.is_pressed("space"):
            force_jump = client + dwForceJump
            if player:
                on_ground = pm.read_int(player + m_fFlags)

                if on_ground and on_ground == 257:
                    pm.write_int(force_jump, 5)
                    time.sleep(0.05)
                    pm.write_int(force_jump, 4)

        time.sleep(0.0002)


if __name__ == '__main__':
    main()
