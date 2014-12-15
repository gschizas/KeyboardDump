#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import yaml
import json

import keyboard_dump
from keyboard_dump.virtual_keys import *

SEP = '\xb7'

kbd_layouts = keyboard_dump.installed_layouts()
_debug = yaml.dump(kbd_layouts)
kbd_layout = [kbd for kbd in kbd_layouts if kbd['name'].startswith('Greek')][0]
greek_layouts = [kbd for kbd in kbd_layouts if 'Greek' in kbd['name']]
german_layouts = [kbd for kbd in kbd_layouts if 'German' in kbd['name']]
english_layouts = [kbd for kbd in kbd_layouts if 'English' in kbd['name']]

# print(kbd_layouts)
# print(json.dumps(kbd_layouts))
# print(greek_layouts)
# print(german_layouts)
# print(english_layouts)
# print(keyboard_dump.current_languages())
# all_layouts = {'Greek': greek_layouts, 'English': english_layouts, 'German': german_layouts}
# print(yaml.dump(all_layouts, default_flow_style=False))
# existing = layout_id in current_languages()
# kbd = _load_keyboard_layout(layout_id)
# yield kbd
# if not existing:
#        _unload_keyboard_layout(kbd)


#def _load_keyboard_layout(layout_id):
#    return ctypes.windll.user32.LoadKeyboardLayoutW(layout_id)


# layout_name = kbd_layout['display']
# print(keyboard_dump.load_indirect_string(layout_name))
# layout_name_2 = layout_name.replace('5046', '5084')
# print(keyboard_dump.load_indirect_string(layout_name_2))
# print(keyboard_dump.installed_layouts())
# print(keyboard_dump.current_languages())

# with keyboard_dump.load_keyboard(kbd_layout['id']) as kbd:
#with keyboard_dump.load_keyboard('04090409') as kbd:
for kbd_id in ('04090409', '04080408', '04070407', '08090409'):
    with keyboard_dump.load_keyboard(kbd_id) as kbd:
        print('=' * 20, keyboard_dump.layout_name(kbd_id), '=' * 20)
        for shift_state in (['normal'], ['shift']):  #, ['alt_gr']):
            # shift_state = ['shift']  # ['control', 'alt_gr', 'shift']
            print('--' * 10, '+'.join(shift_state), '--' * 10)
            print('Row 1:', SEP.join(keyboard_dump.key_values(
                kbd,
                VK_OEM_3, VK_1, VK_2, VK_3, VK_4, VK_5, VK_6, VK_7, VK_8, VK_9, VK_0,
                VK_OEM_MINUS, VK_OEM_PLUS,
                shift_state=shift_state)))
            print('Row 2:   ', SEP.join(keyboard_dump.key_values(
                kbd,
                VK_Q, VK_W, VK_E, VK_R, VK_T, VK_Y, VK_U, VK_I, VK_O, VK_P,
                VK_OEM_4, VK_OEM_6, VK_OEM_5,
                shift_state=shift_state)))
            print('Row 3:    ', SEP.join(keyboard_dump.key_values(
                kbd,
                VK_A, VK_S, VK_D, VK_F, VK_G, VK_H, VK_J, VK_K, VK_L,
                VK_OEM_1, VK_OEM_7, VK_OEM_8,
                shift_state=shift_state)))
            print('Row 4:     ', SEP.join(keyboard_dump.key_values(
                kbd,
                VK_Z, VK_X, VK_C, VK_V, VK_B, VK_N, VK_M,
                VK_OEM_COMMA, VK_OEM_PERIOD, VK_OEM_2,
                shift_state=shift_state)))
            print()
