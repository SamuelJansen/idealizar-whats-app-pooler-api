import pyautogui
pyautogui.FAILSAFE = True

def currentPosition() :
    return pyautogui.position()

def scroll(scrollAmmount) :
    pyautogui.scroll(scrollAmmount)

def moveTo(x, y) :
    pyautogui.moveTo(x, y)
