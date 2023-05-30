import os
import time
import msvcrt
import winreg
import pyautogui
from pynput import keyboard
from pin_codes import pin_codes

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_state(index, language):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\RustCLR', 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\RustCLR')
    winreg.SetValueEx(key, 'last_index', 0, winreg.REG_DWORD, index)
    winreg.SetValueEx(key, 'language', 0, winreg.REG_DWORD, language)
    winreg.CloseKey(key)

def load_state():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\RustCLR', 0, winreg.KEY_READ)
        val, regtype = winreg.QueryValueEx(key, 'last_index')
        lang_val, lang_regtype = winreg.QueryValueEx(key, 'language')
        winreg.CloseKey(key)

        if lang_val in [1, 2, 3]:
            return val, lang_val
    except FileNotFoundError:
        return 0, None

def read_pin_codes():
    return pin_codes.strip().split("\n")

numbers = read_pin_codes()
current_index = 0
last_number = None
last_loop_index = 0  # Numer ostatniej pętli

def load_language():
    language = load_state()[1]
    if language is None:
        print("Wybierz język / Choose language / Wählen Sie die Sprache:")
        print("Polski: 1")
        print("English: 2")
        print("Deutsch: 3")

        while language not in [1, 2, 3]:
            choice = msvcrt.getch()
            if choice in [b'1', b'2', b'3']:
                language = int(choice)
                break
        save_state(current_index, language)

    if language == 1:
        from Language.instructions_pl import print_instructions, print_reset, print_end
    elif language == 2:
        from Language.instructions_en import print_instructions, print_reset, print_end
    elif language == 3:
        from Language.instructions_de import print_instructions, print_reset, print_end

    return print_instructions, print_reset, print_end

print_instructions, print_reset, print_end = load_language()

current_index, language = load_state()
current_index += 1
last_number = numbers[current_index - 1] if current_index - 1 < len(numbers) else None

def perform_action(x_offset):
    global current_index
    global last_number

    if current_index >= len(numbers):
        print("Brak dalszych numerów.")
        return

    pyautogui.keyDown('e')
    time.sleep(0.02)
    pyautogui.move(0, -50)
    time.sleep(0.02)
    pyautogui.move(x_offset, 0)
    time.sleep(0.02)
    pyautogui.click()
    time.sleep(0.02)
    pyautogui.keyUp('e')
    time.sleep(0.03)

    last_number = numbers[current_index]
    for digit in last_number:
        pyautogui.write(digit)
        time.sleep(0.009)
        
    print(f"{current_index + 1}. {last_number}")
    save_state(current_index, language)
    current_index += 1

def repeat_action(x_offset):
    global last_number
    pyautogui.keyDown('e')
    time.sleep(0.02)
    pyautogui.move(0, -50)
    time.sleep(0.02)
    pyautogui.move(x_offset, 0)
    time.sleep(0.02)
    pyautogui.click()
    time.sleep(0.02)
    pyautogui.keyUp('e')
    time.sleep(0.03)
    if last_number is not None:
        for digit in last_number:
            pyautogui.write(digit)
            time.sleep(0.009)

    print(f"{current_index}. {last_number}")


def on_press(key):
    global current_index
    global last_number
    global language
    global last_loop_index

    try:
        if key == keyboard.Key.end:
            print_end()
            return False

        elif key == keyboard.Key.delete:
            current_index = 0
            save_state(current_index, language)
            clear_console()
            print_instructions()
            print_reset()

        elif key == keyboard.Key.f5:
            perform_action(50)

        elif key == keyboard.Key.f9:
            perform_action(-50)

        elif key == keyboard.Key.f6:
            repeat_action(50)

        elif key == keyboard.Key.f10:
            repeat_action(-50)

        elif key == keyboard.Key.f2:
            for _ in range(5):
                perform_action(50)
                time.sleep(1.5)
                last_loop_index = current_index - 1

        elif key == keyboard.Key.f3:
            for _ in range(5):
                perform_action(-50)
                time.sleep(2)
                last_loop_index = current_index - 1

        elif key == keyboard.Key.f7:
            if last_loop_index > 0:
                for i in range(last_loop_index, current_index):
                    perform_action(50)
                    time.sleep(1.5)  # Przerwa 2 sekundy
                last_loop_index = current_index - 1

        elif key == keyboard.Key.f11:
            if last_loop_index > 0:
                for i in range(last_loop_index, current_index):
                    perform_action(-50)
                    time.sleep(1.5)  # Przerwa 2 sekundy
                last_loop_index = current_index - 1

    except AttributeError:
        pass

print_instructions()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()