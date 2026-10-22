# lshell-lite
Simple configuration for swayFX

# Preview
<img width="1919" height="1080" alt="image" src="https://github.com/user-attachments/assets/7b7da370-8f3f-4e65-a07d-bf2edf969e32" />
<img width="1921" height="1080" alt="image" src="https://github.com/user-attachments/assets/58483fc7-85e3-4517-b6f3-ffd0c013ef4d" />

# Wallpapers 
<img width="5000" height="3542" alt="abstract_background_with_flowing_waves_design_0509" src="https://github.com/user-attachments/assets/f2ef7b1b-cf18-42af-b53a-35c6e12cf9ff" />
<img width="3000" height="2000" alt="282" src="https://github.com/user-attachments/assets/2fb61121-765b-488f-bd5b-c59c38c4dc8a" />

### Key Bindings

<details>
<summary>Click to view full keybindings list</summary>



| Keybind | Action | Command |
| :--- | :--- | :--- |
| **Applications** | | |
| `Mod` + `m` | Passwords Manager | `kitty python3 $HOME/.config/passwords.py` |
| `Mod` + `s` | Config Settings | `kitty python3 $HOME/.config/lshell.py` |
| `Mod` + `Enter` | Open Terminal | `$term (Kitty)` |
| `Mod` + `d` | App Launcher | `rofi -show drun` |
| `Mod` + `c` | Crypto Monitor | `kitty python3 $HOME/.config/cryptosee.py` |
| `Mod` + `b` | Browser | `firefox` |
| `Mod` + `n` | File Manager | `dolphin` |
| `Mod` + `w` | Wallpaper Manager | `waypaper` |
| `Mod` + `.` | Emoji Launcher | `rofi -show emoji` |
| `Mod` + `shift` + `e` | Logout Manager | `wlogout` |
| **Navigation & Workspaces** | | |
| `Mod` + `Tab` | Visual Window List | `rofi -show window` |
| **System** | | |
| `Mod` + `q` | Kill Focused Window | `kill` |
| `Mod` + `Shift` + `c` | Reload Configuration | `reload` |
| `Mod` + `Shift` + `e` | Exit Sway | `swaynag` |
| **Screenshots** | | |
| `Mod` + `Shift` + `s` | Region Screenshot | `grim + slurp` |
| **Window Management** | | |
| `Mod` + `Shift` + `Space` | Toggle Floating | `floating toggle` |
| `Mod` + `Shift` + `Minus` | Scratchpad (Move) | `move scratchpad` |
| **Hardware / Media** | | |
| `Vol Up/Down/Mute` | Audio Control | `pactl` |
| `Play/Next/Prev` | Media Control | `playerctl` |


</details>

# Install
## Arch Linux
```bash
cd ~
curl -O https://raw.githubusercontent.com/deploydy/lshell-lite/main/install.sh
chmod +x install.sh
./install.sh
```

# System Requirements

* **OS:** Arch Linux (Arch-based)
* **GPU:** Intel, AMD, or Nvidia with native Wayland support
* **RAM:** 1 GB minimum (2 GB recommended)
* **CPU:** Any modern dual-core processor
* **Storage:** 16 GB or more for comfortable system use

# Once installed, do this
Press Win + S and select the panel position and your city. Press Enter and select item 0 and press Enter again, then reload the config - Win+Shift+C
