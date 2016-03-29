#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import keyboard

kbd_layouts = keyboard.installed_layouts()
kbd_layout = [kbd for kbd in kbd_layouts if kbd['name'].startswith('Greek')][0]
greek_layouts = [kbd for kbd in kbd_layouts if 'Greek' in kbd['name']]
german_layouts = [kbd for kbd in kbd_layouts if 'German' in kbd['name']]
english_layouts = [kbd for kbd in kbd_layouts if kbd['id'].endswith('0409')]

with open('output.txt', 'w', encoding='utf_8_sig') as output_file:
    for kbd_layout in greek_layouts:  # ('04090409', '00020409'):
        kbd_id = kbd_layout['id']
        with keyboard.load_keyboard(kbd_id) as kbd:
            print('=' * 20, keyboard.layout_name(kbd_id) + ' ({})'.format(kbd_id), '=' * 20, file=output_file)
            for shift_state in (['normal'], ['shift'], ['alt_gr'], ['shift', 'alt_gr']):
                row_1 = keyboard.keyboard_row(kbd, keyboard.virtual_keys.VKK_ROW_1, shift_state)
                row_2 = keyboard.keyboard_row(kbd, keyboard.virtual_keys.VKK_ROW_2, shift_state)
                row_3 = keyboard.keyboard_row(kbd, keyboard.virtual_keys.VKK_ROW_3, shift_state)
                row_4 = keyboard.keyboard_row(kbd, keyboard.virtual_keys.VKK_ROW_4, shift_state)
                # shift_state = ['shift']  # ['control', 'alt_gr', 'shift']
                print('--' * 10, '+'.join(shift_state), '--' * 10, file=output_file)
                print('Row 1:', row_1, file=output_file)
                print('Row 2:   ', row_2, file=output_file)
                print('Row 3:    ', row_3, file=output_file)
                print('Row 4:     ', row_4, file=output_file)
                print('', file=output_file)
