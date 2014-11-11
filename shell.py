import yaml

import keyboard_dump
from keyboard_dump.virtual_keys import *


kbd_layouts = keyboard_dump.installed_layouts()
_debug = yaml.dump(kbd_layouts)
kbd_layout = [kbd for kbd in kbd_layouts if kbd['name'].startswith('Polish (2')][0]
# print(kbd_layout)
layout_name = kbd_layout['display']
print(keyboard_dump.load_indirect_string(layout_name))
# layout_name_2 = layout_name.replace('5046', '5084')
# print(keyboard_dump.load_indirect_string(layout_name_2))

kbd = keyboard_dump.load_keyboard_layout(kbd_layout['id'])

shift_state = []  # ['control', 'alt_gr', 'shift']

print('Row 1:', ' '.join(keyboard_dump.key_values(kbd, VK_Q, VK_W, VK_E, VK_R, VK_T, VK_Y, VK_U, VK_I, VK_O, VK_P,
                                                  shift_state=shift_state)))
print('Row 2:', ' '.join(keyboard_dump.key_values(kbd, VK_A, VK_S, VK_D, VK_F, VK_G, VK_H, VK_J, VK_K, VK_L,
                                                  shift_state=shift_state)))
print('Row 3:', ' '.join(keyboard_dump.key_values(kbd, VK_Z, VK_X, VK_C, VK_V, VK_B, VK_N, VK_M,
                                                  shift_state=shift_state)))

keyboard_dump.unload_keyboard_layout(kbd)