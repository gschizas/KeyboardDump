#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import winreg
import win32api
from contextlib import contextmanager
from . import virtual_keys

_installed_layouts = None

dead_key_ref = 0

dead_key_refs = ''.join([chr(x) for x in range(0x2776, 0x2780)]) +  ''.join([chr(x) for x in range(0x24EB, 0x24F5)])

def installed_layouts():
    kbd_layout_root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Keyboard Layouts')
    i = 0
    kbd_layouts = []  # collections.OrderedDict()
    while True:
        try:
            layout_id_text = winreg.EnumKey(kbd_layout_root, i)
            layout_key = winreg.OpenKey(kbd_layout_root, layout_id_text)
            layout_text = winreg.QueryValueEx(layout_key, 'Layout Text')[0]
            layout_display_name = winreg.QueryValueEx(layout_key, 'Layout Display Name')[0]
            i += 1
            winreg.CloseKey(layout_key)
            if layout_display_name.startswith('@'):
                layout_display_name = load_indirect_string(layout_display_name)
            layout_id = int(layout_id_text, 16)
            if layout_id & 0xFFFF0000 == 0:
                layout_id += layout_id << 16
            kbd_layouts.append(dict(id='{0:08x}'.format(layout_id), name=layout_text, display=layout_display_name))
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
    return buff.decode('UTF-16LE').strip('\0')


@contextmanager
def load_keyboard(layout_name):
    layout_id = int(layout_name, 16)
    if layout_id & 0xFFFF0000 == 0:
        layout_id += layout_id << 16
    existing = '{0:08x}'.format(layout_id) in current_languages()
    layout_to_load_hi = (layout_id & 0xFFFF0000) >> 16
    layout_to_load_lo = (layout_id & 0xFFFF)
    if layout_to_load_hi == layout_to_load_lo:
        layout_to_load_hi = 0
    layout_to_load = (layout_to_load_hi << 16) + layout_to_load_lo
    kbd = _load_keyboard_layout('{:08x}'.format(layout_to_load))
    yield kbd
    if not existing:
        _unload_keyboard_layout(kbd)


def _load_keyboard_layout(layout_id):
    return ctypes.windll.user32.LoadKeyboardLayoutW(layout_id, 0)


def _unload_keyboard_layout(kbd):
    ctypes.windll.user32.UnloadKeyboardLayout(kbd)


def key_values(kbd, *keys, shift_state):
    return [key_value(kbd, key, shift_state) for key in keys]


def key_value(kbd, key, shift_state):
    global dead_key_ref
    buff = bytes(256)
    keystate = bytearray(256)
    if 'shift' in shift_state:
        keystate[virtual_keys.VK_SHIFT] = 0x80
    if 'control' in shift_state:
        keystate[virtual_keys.VK_CONTROL] = 0x80
    if 'alt_gr' in shift_state:
        keystate[virtual_keys.VK_CONTROL] = 0x80
        keystate[virtual_keys.VK_MENU] = 0x80
    if 'caps' in shift_state:
        keystate[virtual_keys.VK_CAPITAL] = 0x80

    scan_code = ctypes.windll.user32.MapVirtualKeyExW(key, 3, kbd)
    first_len = ctypes.windll.user32.ToUnicodeEx(key, scan_code, bytes(keystate), buff, 256, 0, kbd)
    result = _decode(buff)
    if first_len < 0:  # dead character?
        #space_scan_code = ctypes.windll.user32.MapVirtualKeyExW(key, 3, kbd)
        #ctypes.windll.user32.ToUnicodeEx(
        #    virtual_keys.VK_SPACE, space_scan_code, bytes(bytearray(256)), buff, 256, 0, kbd)
        #result = '\u2588' + result # + '\u2591' + _decode(buff)
        result = dead_key_refs[dead_key_ref]
        dead_key_ref += 1        
    elif result == '':
        result = '\u00a0'
    return result


def current_languages():
    return ['{0:08x}'.format(ctypes.c_uint(kbd).value) for kbd in win32api.GetKeyboardLayoutList()]
    # int keyboardLayoutList = SafeNativeMethods.GetKeyboardLayoutList(0, (IntPtr[]) null);
    # IntPtr[] hkls = new IntPtr[keyboardLayoutList];
    # SafeNativeMethods.GetKeyboardLayoutList(keyboardLayoutList, hkls);
    # InputLanguage[] inputLanguageArray = new InputLanguage[keyboardLayoutList];
    # for (int index = 0; index < keyboardLayoutList; ++index)
    # inputLanguageArray[index] = new InputLanguage(hkls[index]);
    # return new InputLanguageCollection(inputLanguageArray);


def _decode(buff):
    return buff.decode('utf-16le').strip('\0')


def layout_name(kbd_id):
    global _installed_layouts
    if _installed_layouts is None:
        _installed_layouts = installed_layouts()
    keyboards = [kbd for kbd in _installed_layouts if kbd['id'] == kbd_id]
    if keyboards:
        return keyboards[0]['display']
    else:
        return '?' + kbd_id + '?'
