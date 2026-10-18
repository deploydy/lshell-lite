#!/usr/bin/env python3
import json
import re
import os
import sys
import time
import subprocess

CONFIG_PATH = os.path.expanduser("~/.config/waybar/config")
STYLE_PATH = os.path.expanduser("~/.config/waybar/style.css")

ASCII_LOGO = [
    r"  _          _          _ _ ",
    r" | |___  ___| |_  ___| | |",
    r" | (_-< / _| ' \/ -_) | |",
    r" |_/__/ \__|_||_\___|_|_|",
    r"          L I T E        "
]

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def print_centered_logo():
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    
    print("\n")
    for line in ASCII_LOGO:
        print(line.center(columns))
    print("\n" + "─" * columns + "\n")

def show_loading_animation(text="Applying changes"):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    print()
    for _ in range(15):
        for frame in frames:
            sys.stdout.write(f"\r  \033[1;36m{frame}\033[0m {text}...")
            sys.stdout.flush()
            time.sleep(0.015)
    sys.stdout.write(f"\r  \033[1;32m✔\033[0m {text} completed!     \n")
    sys.stdout.flush()

def reload_waybar():
    show_loading_animation("Reloading Waybar")
    subprocess.run("killall waybar; waybar &", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def load_json_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"  [-] File {CONFIG_PATH} not found!")
        return None
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def change_color():
    color = input("  Enter hex color (e.g., #ffffff, #ff5555, #89b4fa): ").strip()
    if not re.match(r"^#[0-9a-fA-F]{6}$", color):
        print("  [-] Invalid hex color format!")
        return
    
    if os.path.exists(STYLE_PATH):
        with open(STYLE_PATH, "r", encoding="utf-8") as f:
            css = f.read()
        
        new_css = re.sub(r'(\*\s*\{[^}]*color:\s*)[^;]+(;)', r'\1' + color + r'\2', css)
        
        with open(STYLE_PATH, "w", encoding="utf-8") as f:
            f.write(new_css)
        
        reload_waybar()
    else:
        print(f"  [-] File {STYLE_PATH} not found!")

def toggle_position():
    data = load_json_config()
    if not data:
        return
    
    current = data.get("position", "top")
    new_pos = "bottom" if current == "top" else "top"
    data["position"] = new_pos
    
    save_json_config(data)
    reload_waybar()

def change_timezone():
    data = load_json_config()
    if not data:
        return
    
    print("  Examples: Europe/Kyiv, Europe/London, America/New_York, UTC")
    tz = input("  Enter Region/City: ").strip()
    
    if not tz:
        print("  [-] Timezone cannot be empty!")
        return
    
    if "clock" not in data:
        data["clock"] = {}
    
    data["clock"]["timezone"] = tz
    save_json_config(data)
    reload_waybar()

def main():
    while True:
        clear_screen()
        print_centered_logo()
        print("  1. Change text and icon color")
        print("  2. Toggle panel position (top / bottom)")
        print("  3. Change timezone / city")
        print("  0. Exit\n")
        
        choice = input("  Select an option [0-3]: ").strip()
        
        if choice == "1":
            change_color()
            input("\n  Press Enter to continue...")
        elif choice == "2":
            toggle_position()
            input("\n  Press Enter to continue...")
        elif choice == "3":
            change_timezone()
            input("\n  Press Enter to continue...")
        elif choice == "0":
            clear_screen()
            break

if __name__ == "__main__":
    main()
