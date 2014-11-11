#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import winreg


def installed_layouts():
    kbd_layout_root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Keyboard Layouts')
    i = 0
    kbd_layouts = []  # collections.OrderedDict()
    while True:
        try:
            layout_id = winreg.EnumKey(kbd_layout_root, i)
            layout_key = winreg.OpenKey(kbd_layout_root, layout_id)
            layout_name = winreg.QueryValueEx(layout_key, 'Layout Text')[0]
            layout_display_name = winreg.QueryValueEx(layout_key, 'Layout Display Name')[0]
            i += 1
            winreg.CloseKey(layout_key)
            kbd_layouts.append(dict(id=layout_id, name=layout_name, display=layout_display_name))
        except OSError as e:
            if e.winerror == 259:
                break
            else:
                raise
    winreg.CloseKey(kbd_layout_root)
    return kbd_layouts


def load_indirect_string(name):
    buff = bytes(256)
    shlwapi = ctypes.windll.LoadLibrary('C:/Windows/system32/shlwapi.dll')
    shlwapi.SHLoadIndirectString(name, buff, 256, None)
    return buff.decode('UTF-16LE')


def load_keyboard_layout(layout_id):
    kbd = ctypes.windll.user32.LoadKeyboardLayoutW(layout_id)
    return kbd


def unload_keyboard_layout(kbd):
    ctypes.windll.user32.UnloadKeyboardLayout(kbd)


def key_values(kbd, *keys, shift_state):
    return [key_value(kbd, key, shift_state) for key in keys]


def key_value(kbd, key, shift_state):
    buff = bytes(256)
    keystate = bytearray(256)
    if 'shift' in shift_state:
        keystate[16] = 0x80
    if 'control' in shift_state:
        keystate[17] = 0x80
    if 'alt_gr' in shift_state:
        keystate[18] = 0x80
    if 'caps' in shift_state:
        keystate[20] = 0x80

    scan_code = ctypes.windll.user32.MapVirtualKeyExW(key, 3, kbd)
    result = ctypes.windll.user32.ToUnicodeEx(key, scan_code, bytes(keystate), buff, 256, 0, kbd)
    return _decode(buff)

    print()
    print(ctypes.windll.user32.MapVirtualKeyExW(0, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(1, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(2, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(3, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(13, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(14, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(18, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(14, 2, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(65, 2, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(65, 0, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(0x14, 0, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(65, 2, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(65, 4, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(65, 3, kbd))
    print(ctypes.windll.user32.MapVirtualKeyExW(0x30, 3, kbd))


def _decode(buff):
    return buff.decode('utf-16le').strip('\0')