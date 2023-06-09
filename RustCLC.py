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
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\RustCLC', 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\RustCLC')
    winreg.SetValueEx(key, 'last_index', 0, winreg.REG_DWORD, index)
    winreg.SetValueEx(key, 'language', 0, winreg.REG_DWORD, language)
    winreg.CloseKey(key)

def load_state():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\RustCLC', 0, winreg.KEY_READ)
        val, regtype = winreg.QueryValueEx(key, 'last_index')
        lang_val, lang_regtype = winreg.QueryValueEx(key, 'language')
        winreg.CloseKey(key)

        if lang_val in [1, 2, 3, 4]:  # uwzględnienie wszystkich 4 możliwych wartości dla lang_val
            return val, lang_val
    except FileNotFoundError:
        pass

    return 0, None

def read_pin_codes():
    return list(enumerate(pin_codes.strip().split("\n"), start=1))

# Query number of users and order of the user
def query_users():
    print("How many users (1-8)?")
    users = 0
    while users not in range(1, 9):
        choice = msvcrt.getch()
        if choice in [bytes(str(i), 'utf-8') for i in range(1, 9)]:
            users = int(choice)
            break
    return users

def query_user_order(users):
    print(f"Which one of these {users} are you?")
    user_order = 0
    while user_order not in range(1, users+1):
        choice = msvcrt.getch()
        if choice in [bytes(str(i), 'utf-8') for i in range(1, users+1)]:
            user_order = int(choice)
            clear_console()
            break
    return user_order

users = query_users()
user_order = query_user_order(users)

numbers = read_pin_codes()[user_order-1::users]

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
        print("Français: 4")

        while language not in [1, 2, 3, 4]:
            choice = msvcrt.getch()
            if choice in [b'1', b'2', b'3', b'4']:
                language = int(choice)
                break
        save_state(current_index, language)

    if language == 1:
        from Language.instructions_pl import print_instructions, print_reset, print_end
    elif language == 2:
        from Language.instructions_en import print_instructions, print_reset, print_end
    elif language == 3:
        from Language.instructions_de import print_instructions, print_reset, print_end
    elif language == 4:
        from Language.instructions_fr import print_instructions, print_reset, print_end

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
    for digit in last_number[1]:
        pyautogui.write(digit)
        time.sleep(0.009)
        
    print(f"{last_number[0]}. {last_number[1]}")
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
        for digit in last_number[1]:
            pyautogui.write(digit)
            time.sleep(0.009)

    print(f"{last_number[0]}. {last_number[1]}")

def change_language():
    global print_instructions, print_reset, print_end, language
    language = None
    save_state(current_index, language)
    print_instructions, print_reset, print_end = load_language()


currently_pressed_keys = set()

def handle_key_press(key):
    global current_index
    global last_number
    global language
    global last_loop_index
    global currently_pressed_keys
    global print_instructions, print_reset, print_end

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

        elif key == keyboard.KeyCode.from_char('l') and (keyboard.Key.alt_l in currently_pressed_keys or keyboard.Key.alt_r in currently_pressed_keys):
            clear_console()
            language = change_language()
            print_instructions, print_reset, print_end = load_language()
            print_instructions()

        ### Powtórzenie poprzedniego indexu ###
        #__Dla drzwi__#
        elif key == keyboard.Key.f5 and (keyboard.Key.ctrl_l in currently_pressed_keys or keyboard.Key.ctrl_r in currently_pressed_keys): 
            repeat_action(50)

        #__Dla bram__#
        elif key == keyboard.Key.f8 and (keyboard.Key.ctrl_l in currently_pressed_keys or keyboard.Key.ctrl_r in currently_pressed_keys):
            repeat_action(-50)

        ### Wywaołanie kolejnego indexu ###
        #__Dla drzwi__#
        elif key == keyboard.Key.f5:
            perform_action(50)

        #__Dla bram__#
        elif key == keyboard.Key.f8:
            perform_action(-50)

        ### Wywołanie 5 poprzednich indeksów ###
        #_Dla drzwi_#
        elif key == keyboard.Key.f1 and (keyboard.Key.ctrl_l in currently_pressed_keys or keyboard.Key.ctrl_r in currently_pressed_keys):
            prev_index = current_index
            current_index = max(0, current_index - 5)
            save_state(current_index, language)
            actions_taken = min(5, prev_index - current_index)
            for _ in range(actions_taken):
                perform_action(50)
                time.sleep(1.5)
            last_loop_index = current_index - 1

            for _ in range(5 - actions_taken):
                if current_index < len(numbers):
                    perform_action(50)
                    time.sleep(1.5)
        
        #_Dla bram_#
        elif key == keyboard.Key.f4 and (keyboard.Key.ctrl_l in currently_pressed_keys or keyboard.Key.ctrl_r in currently_pressed_keys):
            prev_index = current_index
            current_index = max(0, current_index - 5)
            save_state(current_index, language)
            actions_taken = min(5, prev_index - current_index)
            for _ in range(actions_taken):
                perform_action(-50)
                time.sleep(1.5)
            last_loop_index = current_index - 1

            for _ in range(5 - actions_taken):
                if current_index < len(numbers):
                    perform_action(50)
                    time.sleep(1.5)

        ### Wywoałnie w pętli kolejnych 5 indexów ###
        #__Dla drzwi__#
        elif key == keyboard.Key.f1:
            for _ in range(5):
                perform_action(50)
                time.sleep(1.5)
                last_loop_index = current_index - 1

        elif key == keyboard.Key.f4:
            for _ in range(5):
                perform_action(-50)
                time.sleep(1.5)
                last_loop_index = current_index - 1

    except AttributeError:
        pass

def change_language():
    language = None
    print("Wybierz język / Choose language / Wählen Sie die Sprache:")
    print("Polski: 1")
    print("English: 2")
    print("Deutsch: 3")
    print("Français: 4")

    while language not in [1, 2, 3, 4]:
        choice = msvcrt.getch()
        if choice in [b'1', b'2', b'3', b'4']:
            language = int(choice)
            break
    save_state(current_index, language)
    clear_console()
    return language

def on_press(key):
    currently_pressed_keys.add(key)
    handle_key_press(key)

def on_release(key):
    try:
        currently_pressed_keys.remove(key)
    except KeyError:
        pass

print_instructions()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()