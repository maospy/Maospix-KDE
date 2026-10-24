#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="maospix-kde"
iso_label="MAOSPIX_KDE_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"
iso_publisher="maospytek <https://github.com/maospy>"
iso_application="maospix-kde Live/Rescue"
iso_version="$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y.%m.%d)"
install_dir="arch"
bootmodes=('bios.syslinux'
           'uefi.systemd-boot')
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86,arm64' '-b' '1M' '-Xdict-size' '1M')
bootstrap_tarball_compression=('zstd' '-c' '-T0' '--auto-threads=logical' '--long' '-19')
kernel_params_aarch64="clk_ignore_unused pd_ignore_unused arm64.nopauth"
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/root/.automated_script.sh"]="0:0:755"
  ["/root/.gnupg"]="0:0:700"
  ["/usr/local/bin/choose-mirror"]="0:0:755"
  ["/usr/local/bin/Installation_guide"]="0:0:755"
  ["/usr/local/bin/livecd-sound"]="0:0:755"
  ["/etc/gshadow"]="0:0:400"
  ["/etc/sudoers.d"]="0:0:750"
  ["/etc/sudoers.d/g_wheel"]="0:0:440"
  ["/home/liveuser"]="1000:1000:750"
  ["/home/liveuser/Desktop"]="1000:1000:755"
  ["/home/liveuser/.config"]="1000:1000:755"
  ["/home/liveuser/.config/ghostty"]="1000:1000:755"
  ["/home/liveuser/.config/brave-flags.conf"]="1000:1000:644"
  ["/home/liveuser/.config/ghostty/config"]="1000:1000:644"
  ["/home/liveuser/Desktop/instalar-maospix.desktop"]="1000:1000:755"
  ["/usr/local/bin/maospix-postinstall"]="0:0:755"
  ["/usr/local/bin/maospix-terminal"]="0:0:755"
  ["/usr/local/bin/maospix-postboot"]="0:0:755"
  ["/usr/local/bin/maospix-hello"]="0:0:755"
  ["/usr/local/bin/maospix-nvidia"]="0:0:755"
)
