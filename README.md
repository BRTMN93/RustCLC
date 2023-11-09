# RustCLC (Code Lock Cracker)
RustCLC is an automation tool designed to type in pin codes in a game. This tool helps to automate the repetitive task of typing in pin codes, thus saving time and reducing potential for human error.

## Prerequisites
Python 3
Python libraries: pyautogui and pynput
A module named pin_codes that contains the list of pin codes
You can install the required Python libraries using pip:
***pip install pyautogui pynput***

## How to Use
Start the program by running the script.

A prompt will ask you to input the number of users. You can select between 1 and 8 by pressing the corresponding number key.

Next, you will be asked to select your user order. Again, input the corresponding number key.

The system will now read your pin codes.

You can select the language of your choice for the prompts. The options are: Polish (1), English (2), German (3), and French (4).

To perform actions or repeat actions, you can use different key combinations as described below:

**F4:** Perform action for doors.

**F8:** Perform action for gates.

**Ctrl + F4:** Repeat the last action for doors.

**Ctrl + F8:** Repeat the last action for gates.

**F5:** Perform the next 5 actions for doors.

**F9:** Perform the next 5 actions for gates.

**Ctrl + F5:** Perform the previous 5 actions for doors.

**Ctrl + F9:** Perform the previous 5 actions for gates.

**Alt + L:** Change the language of prompts.

**Alt+Delete:** Reset the program.

**End:** Quit the program.

***Remember, your progress is saved in the Windows Registry (HKEY_CURRENT_USER\SOFTWARE\RustCLC), so you can resume the program at a later time.***

## Disclaimer
This tool is designed to only be used where automated entry of pin codes is allowed by the game's rules and guidelines. Users are solely responsible for any potential rule violations.
