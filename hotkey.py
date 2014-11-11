#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# After a post to c.l.py by Richie Hindle:
# http://groups.google.com/groups?th=80e876b88fabf6c9
#
import os
import ctypes
from ctypes import wintypes
import win32ui
import win32gui
import win32api

import win32con


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def handle_win_f3():
    os.startfile(os.environ['TEMP'])


def handle_win_f10():
    user32.PostQuitMessage(0)


def handle_win_f5():
    wnd = win32ui.GetForegroundWindow()
    print(wnd.GetWindowText())
    print(get_selected_text_from_front_window())


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_ulong),
        ("top", ctypes.c_ulong),
        ("right", ctypes.c_ulong),
        ("bottom", ctypes.c_ulong)
    ]


class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("hwndActive", ctypes.c_ulong),
        ("hwndFocus", ctypes.c_ulong),
        ("hwndCapture", ctypes.c_ulong),
        ("hwndMenuOwner", ctypes.c_ulong),
        ("hwndMoveSize", ctypes.c_ulong),
        ("hwndCaret", ctypes.c_ulong),
        ("rcCaret", RECT)
    ]


def get_selected_text_from_front_window():
    wnd = win32ui.GetForegroundWindow()
    txt = get_window_text(wnd, True)
    return txt


def get_window_text(handle, selected=False):  # As String
    txt = ""
    if handle:
        buf_size = 1 + win32gui.SendMessage(handle, win32con.WM_GETTEXTLENGTH, 0, 0)
        if buf_size:
            buffer = win32gui.PyMakeBuffer(buf_size)
            win32gui.SendMessage(handle, win32con.WM_GETTEXT, buf_size, buffer)
            txt = buffer[:buf_size]

        if selected and buf_size:
            selinfo = win32gui.SendMessage(handle, win32con.EM_GETSEL, 0, 0)
            endpos = win32api.HIWORD(selinfo)
            startpos = win32api.LOWORD(selinfo)
            return txt[startpos: endpos]

    return txt


def main():
    global byref, user32, HOTKEYS, HOTKEY_ACTIONS
    byref = ctypes.byref
    user32 = ctypes.windll.user32

    HOTKEYS = {
        1: (win32con.VK_F3, win32con.MOD_WIN),
        2: (win32con.VK_F10, win32con.MOD_WIN),
        3: (win32con.VK_F5, win32con.MOD_WIN)
    }
    HOTKEY_ACTIONS = {
        1: handle_win_f3,
        2: handle_win_f10,
        3: handle_win_f5
    }

    #
    # RegisterHotKey takes:
    # Window handle for WM_HOTKEY messages (None = this thread)
    # arbitrary id unique within the thread
    # modifiers (MOD_SHIFT, MOD_ALT, MOD_CONTROL, MOD_WIN)
    # VK code (either ord ('x') or one of win32con.VK_*)
    #
    for hotkey_id, (vk, modifiers) in HOTKEYS.items():
        print("Registering id", hotkey_id, "for key", vk)
        if not user32.RegisterHotKey(None, hotkey_id, modifiers, vk):
            print("Unable to register id", hotkey_id)

    #
    # Home-grown Windows message loop: does
    # just enough to handle the WM_HOTKEY
    # messages and pass everything else along.
    #
    try:
        msg = wintypes.MSG()
        while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                action_to_take = HOTKEY_ACTIONS.get(msg.wParam)
                if action_to_take:
                    action_to_take()

            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageA(byref(msg))

    finally:
        for hotkey_id in HOTKEYS.keys():
            user32.UnregisterHotKey(None, hotkey_id)


if __name__ == '__main__':
    main()
