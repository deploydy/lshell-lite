#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }

if [ "$EUID" -eq 0 ]; then
    log_error "Do not run this script as root!"
    exit 1
fi

if ! command -v pacman &> /dev/null; then
    log_error "pacman not found. This script requires Arch Linux."
    exit 1
fi

if ! command -v yay &> /dev/null; then
    log_error "yay is not installed."
    exit 1
fi

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Select an action:${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "  ${GREEN}1)${NC} Update system"
echo -e "  ${GREEN}2)${NC} Full installation"
echo -e "  ${GREEN}3)${NC} Exit"
echo -e "${BLUE}============================================${NC}"
echo ""

while true; do
    read -rp "Your choice [1/2/3]: " CHOICE
    case "$CHOICE" in
        1) ACTION="update"; break ;;
        2) ACTION="install"; break ;;
        3) log_info "Exiting."; exit 0 ;;
        *) echo "Enter 1, 2 or 3." ;;
    esac
done

# ============================================================
# UPDATE
# ============================================================
if [ "$ACTION" = "update" ]; then

    log_info "Updating package databases..."
    sudo pacman -Syy
    log_ok "Databases updated."

    log_info "Updating packages..."
    CONFLICTS=$(sudo pacman -Su --print 2>&1 | grep -iE "conflict" || true)

    if [ -n "$CONFLICTS" ]; then
        log_warn "Conflicts detected:"
        echo "$CONFLICTS"
        echo ""
        read -rp "Remove conflicting packages? [y/N]: " CONFLICT_CHOICE
        if [[ "$CONFLICT_CHOICE" =~ ^[Yy]$ ]]; then
            PKGS=$(echo "$CONFLICTS" | grep -oP '^\s*\K[^:]+(?=\s*:)' || true)
            if [ -n "$PKGS" ]; then
                log_info "Removing: $PKGS"
                sudo pacman -Rdd --noconfirm $PKGS || true
                log_ok "Removed."
            fi
        fi
    fi

    sudo pacman -Su --noconfirm
    log_ok "Packages updated."

    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}  Update completed!${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""

    read -rp "Reboot now? [y/N]: " REBOOT_CHOICE
    if [[ "$REBOOT_CHOICE" =~ ^[Yy]$ ]]; then
        log_info "Rebooting..."
        sudo reboot
    else
        log_info "Reboot skipped. Please reboot manually later."
        exit 0
    fi
fi

# ============================================================
# FULL INSTALL
# ============================================================
log_info "Updating system..."
sudo pacman -Syyu --noconfirm
log_ok "System updated."

log_info "Installing pacman packages..."
sudo pacman -S --needed --noconfirm \
    git autotiling swaybg waybar kitty rofi \
    papirus-icon-theme ttf-fira-code ttf-jetbrains-mono-nerd \
    ttf-nerd-fonts-symbols ttf-font-awesome noto-fonts-emoji \
    gsimplecal wtype rofi-emoji dolphin bluez bluez-utils blueman \
    nwg-displays fastfetch python python-pip polkit-gnome \
    python-cryptography python-requests python-beautifulsoup4 \
    python-rich wl-clipboard
log_ok "Pacman packages installed."

log_info "Installing AUR packages..."
yay -S --needed --noconfirm waypaper wlogout grim slurp
log_ok "AUR packages installed."

BUILD_DIR=$(mktemp -d)

log_info "Building scenefx0.5..."
cd "$BUILD_DIR"
git clone https://aur.archlinux.org/scenefx0.5.git
cd scenefx0.5
makepkg -si --noconfirm
log_ok "scenefx0.5 installed."

log_info "Building swayfx..."
cd "$BUILD_DIR"
git clone https://aur.archlinux.org/swayfx.git
cd swayfx
makepkg -si --noconfirm
log_ok "swayfx installed."

cd ~
rm -rf "$BUILD_DIR"

log_info "Generating fastfetch config..."
fastfetch --gen-config
log_ok "fastfetch config generated."

log_info "Removing old waybar config..."
rm -rf ~/.config/waybar/config.jsonc
log_ok "Old waybar config removed."

log_info "Cloning lshell..."
cd ~
rm -rf "$HOME/lshell"
git clone https://github.com/deploydy/lshell
log_ok "Repository cloned."

log_info "Copying configs..."
mkdir -p ~/.config
cp -r ~/lshell/* ~/.config/
log_ok "Configs copied."

rm -rf ~/lshell
log_ok "Temporary directory removed."

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Installation completed successfully!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""

read -rp "Reboot the system now? [y/N]: " REBOOT_CHOICE
if [[ "$REBOOT_CHOICE" =~ ^[Yy]$ ]]; then
    log_info "Rebooting system..."
    sudo reboot
else
    log_info "Reboot skipped. Please reboot manually later."
    exit 0
fi
