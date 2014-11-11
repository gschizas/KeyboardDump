import win32gui
import sys
from datetime import time

import win32con


def _windowEnumerationHandler(hwnd, resultList):
    """Handler to enumerate the window with param hwnd
Returns resultsList; the window details as an array,
with hwnd, text and class

    :param hwnd:
    :param resultList:
    """
    resultList.append((hwnd,
                       win32gui.GetWindowText(hwnd),
                       win32gui.GetClassName(hwnd)))


def searchChildWindows(hwnd):
    """Recursive function, checks the text of all the children of
the window with handle param hwnd until it reaches the text that
we require, returns the String of this data"""

    childWindows = []
    try:
        # get child windows
        win32gui.EnumChildWindows(hwnd, _windowEnumerationHandler, childWindows)
    except win32gui.error as exception:
        # This seems to mean that the control does not or cannot have child windows
        return

    # get details of each child window
    for childHwnd, windowText, windowClass in childWindows:
        # create text buffer
        buf_size = 2 + win32gui.SendMessage(childHwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        print(buf_size)
        buffer = win32gui.PyMakeBuffer(buf_size)
        # get text from Window using hardware call. (getWindowText() did not return anything)
        win32gui.SendMessage(childHwnd, win32con.WM_GETTEXT, buf_size, buffer)
        # check to see if it's the data we want...
        # print(_decode(buffer[0:buf_size]))
        # .tobytes()
        #if len(buffer) > 2:
        #print(_decode(buffer.tobytes()))
        print(buffer.tobytes())
        if windowStartText in buffer[0:buf_size]:
            return int(childHwnd)

            # return the hwnd
            # global chatHwnd
            # chatHwnd = childHwnd
            #else recurse, checking this window for children
            #might not be needed...
            #searchChildWindows(childHwnd)


def _decode(buff):
    return buff.decode('utf-16le').strip('\0')


def main():
    # declare global
    global chatHwnd, windowTitleText, windowStartText
    results = []
    topWindows = []
    chatHwnd = 0
    windowTitleText = "Untitled - Notepad"
    # The text that the wanted window string begins with, so we can find it
    windowStartText = "Untitled"
    # enumerate all open windows, return topWindows
    win32gui.EnumWindows(_windowEnumerationHandler, topWindows)
    # check each window to fin the one we need
    for hwnd, windowText, windowClass in topWindows:
        if windowText.find(windowTitleText) > -1:
            # search the child windows
            # save the window handle
            chatHwnd = searchChildWindows(hwnd)
            # set the appropriate window focus (if needed)
            # win32gui.SetFocus(hwnd)
            win32gui.SetForegroundWindow(hwnd)

            initBuff = 0
            # get text
            print(chatHwnd)
            while chatHwnd is not None and chatHwnd > 0:

                buf_size = 1 + win32gui.SendMessage(chatHwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
                buffer = win32gui.PyMakeBuffer(buf_size)
                # send a win GETTEXT request to the window and read into buffer
                win32gui.SendMessage(chatHwnd, win32con.WM_GETTEXT, buf_size, buffer)
                if buf_size - initBuff > 1:
                    print(buffer[initBuff:buf_size])

                initBuff = buf_size
                # after 5 seconds, get any new text
                time.sleep(5)
                # needed for Java to read the output correctly
                sys.stdout.flush()


if __name__ == '__main__':
    main()
