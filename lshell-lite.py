#!/usr/bin/env python3
import json
import re
import os
import sys
import time
import shutil
import subprocess

CONFIG_PATH = os.path.expanduser("~/.config/waybar/config")
STYLE_PATH = os.path.expanduser("~/.config/waybar/style.css")

ASCII_LOGO = [
    r"  _     ____  _   _ _____ _     _     ",
    r" | |   / ___|| | | | ____| |   | |    ",
    r" | |   \___ \| |_| |  _| | |   | |    ",
    r" | |___ ___) |  _  | |___| |___| |___ ",
    r" |_____|____/|_| |_|_____|_____|_____|",
    r"              L I T E                  "
]

def clear_screen():
    subprocess.run(["clear"] if os.name == "posix" else ["cls"], check=False)

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
    subprocess.run(["killall", "waybar"], stderr=subprocess.DEVNULL, check=False)
    time.sleep(0.3)
    subprocess.Popen(
        ["waybar"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

def load_json_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"  [-] File {CONFIG_PATH} not found!")
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"  [-] JSON error: {e}")
        return None

def save_json_config(data):
    if os.path.exists(CONFIG_PATH):
        shutil.copy2(CONFIG_PATH, CONFIG_PATH + ".bak")
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def strip_box_shadow():
    if not os.path.exists(STYLE_PATH):
        return
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    new_css = re.sub(r'(?m)^\s*box-shadow\s*:[^;]+;\s*\n?', '', css)
    if new_css != css:
        shutil.copy2(STYLE_PATH, STYLE_PATH + ".bak")
        with open(STYLE_PATH, "w", encoding="utf-8") as f:
            f.write(new_css)

def change_color():
    color = input("  Enter hex color (e.g., #ffffff, #ff5555, #89b4fa): ").strip()
    if not re.match(r"^#[0-9a-fA-F]{6}$", color):
        print("  [-] Invalid hex color format!")
        return
    if not os.path.exists(STYLE_PATH):
        print(f"  [-] File {STYLE_PATH} not found!")
        return
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    new_css = re.sub(r'(?m)^(\s*color:\s*)[^;]+(;)', r'\1' + color + r'\2', css, count=1)
    if new_css == css:
        print("  [-] Could not find color property in style.css")
        return
    shutil.copy2(STYLE_PATH, STYLE_PATH + ".bak")
    with open(STYLE_PATH, "w", encoding="utf-8") as f:
        f.write(new_css)
    reload_waybar()

def toggle_position():
    data = load_json_config()
    if not data:
        return
    current = data.get("position", "top")
    data["position"] = "bottom" if current == "top" else "top"
    save_json_config(data)
    strip_box_shadow()
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
    try:
        from zoneinfo import ZoneInfo
        ZoneInfo(tz)
    except Exception:
        print("  [-] Invalid timezone!")
        return
    if "clock" not in data:
        data["clock"] = {}
    data["clock"]["timezone"] = tz
    save_json_config(data)
    reload_waybar()

def main():
    strip_box_shadow()
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
