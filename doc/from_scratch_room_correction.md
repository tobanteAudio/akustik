# Room Correction

## ArchLinux Install

```sh
# Add user (admin)
pacman -S sudo vim
useradd -m -G wheel tobante
EDITOR=vim visudo

# SSH
sudo pacman -S openssh
sudo systemctl start sshd
sudo systemctl enable sshd
ip addr show

# ALSA
sudo pacman -S alsa-utils
sudo alsamixer
sudo aplay -L | grep :CARD

# JUCE
sudo pacman -S git gcc cmake ninja pkgconf libcurl-gnutls freetype2 fontconfig libx11 libxcomposite libxcb libxrandr libxinerama libxcursor webkit2gtk

# i3
# https://learn.arm.com/learning-paths/laptops-and-desktops/pinebook-pro/i3/
sudo pacman -Sy xorg xorg-xinit dmenu ttf-liberation alacritty i3
echo "exec i3" >> ~/.xinitrc
startx
```

- <https://chatgpt.com/share/67de25d5-a858-8003-8ab8-a88e357e6445>
- <https://chatgpt.com/share/67e7264e-7598-8003-bbbb-c28721e85855>
- <https://chatgpt.com/share/67e72670-dfe8-8003-94ec-e005df305e44>
- <https://chatgpt.com/share/67e72697-0648-8003-87c5-1e01be317446>
