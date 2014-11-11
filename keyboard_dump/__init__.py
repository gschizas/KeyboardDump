#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import winreg
import win32api


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
    kbd = win32api.LoadKeyboardLayout(layout_id)
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


def installed_languages():
    return ['{0:08x}'.format(kbd) for kbd in win32api.GetKeyboardLayoutList() if kbd > 0]
    # int keyboardLayoutList = SafeNativeMethods.GetKeyboardLayoutList(0, (IntPtr[]) null);
    # IntPtr[] hkls = new IntPtr[keyboardLayoutList];
    # SafeNativeMethods.GetKeyboardLayoutList(keyboardLayoutList, hkls);
    # InputLanguage[] inputLanguageArray = new InputLanguage[keyboardLayoutList];
    # for (int index = 0; index < keyboardLayoutList; ++index)
    # inputLanguageArray[index] = new InputLanguage(hkls[index]);
    # return new InputLanguageCollection(inputLanguageArray);


def _decode(buff):
    return buff.decode('utf-16le').strip('\0')