# Maospix-KDE: guía y historia de construcción, desde cero

Autor: Marcos Olmedo (maospytek), Itauguá, Paraguay. Base: Arch Linux + KDE Plasma, construida con archiso e instalador gráfico Calamares. Documento actualizado el 25/10/2026 (ISO 10, versión final).

## 1. Idea y reglas del proyecto

- Distro propia, parte de la familia maospix (antes: maospix-bspwm sobre Fedora y maospy-hypr sobre Arch + Hyprland).
- Estilo Xero Linux / Garuda: todo preinstalado y tematizado, con instalador gráfico.
- Todos los proyectos nuevos se llaman maospix-*.
- Se trabaja de a un paso: se prueba el comando, se confirma el resultado y recién se sigue.

## 2. Entorno de trabajo

- Banco de trabajo: PC con Arch Linux minimal (usuario maospy, carpeta ~/maospix-kde), accesible por SSH desde Windows. 2 núcleos, HDD y 7,6 GB de RAM: cada build tarda unos 40 minutos por la compresión xz y el disco lento.
- Regla: no instalar la ISO en el disco de esta máquina. Un SSD M.2 con Omarchy instalado no se toca.
- Pruebas en VirtualBox en Windows (ISO en C:\ISOs\). Marcos pasa archivos y capturas con scp.

## 3. Paso a paso desde cero

### 3.1 Preparar el equipo de construcción
1. Instalar Arch Linux minimal, crear el usuario y activar SSH.
2. Instalar las herramientas: `sudo pacman -S archiso git base-devel tmux`.
3. Crear la carpeta del proyecto y el repositorio git: `mkdir ~/maospix-kde && cd ~/maospix-kde && git init`.

### 3.2 Perfil archiso
1. Copiar el perfil base: `cp -r /usr/share/archiso/configs/releng ~/maospix-kde/archiso`.
2. En `archiso/profiledef.sh`: `iso_name="maospix-kde"`, publisher y application propios. La tabla `file_permissions` lista los archivos que necesitan permisos (carpeta de liveuser, scripts de /usr/local/bin, configuración de Ghostty, etc.). Cada script nuevo hay que agregarlo ahí con modo 0:0:755.
3. En `archiso/packages.x86_64` (181 paquetes): KDE Plasma, SDDM, Calamares, Brave, Ghostty, Konsole, fastfetch, Papirus, Discover, Flatpak, snapper, grub-btrfs, zram-generator, virtualbox-guest-utils, etc.
4. El live se hace con un usuario `liveuser` (con autologin en SDDM) creado desde `airootfs/etc/passwd`, `shadow`, `group` y `sudoers.d`.

### 3.3 Repositorio local para paquetes de AUR
- archiso no puede usar AUR directamente. Se construyen los paquetes con `makepkg -s` a partir de los PKGBUILD de `pkgbuilds/` (calamares 3.4.2, brave-bin, cliamp-bin) y se agregan a `repo/` con `repo-add repo/maospix-local.db.tar.gz repo/*.pkg.tar.zst`.
- En `archiso/pacman.conf` se declara la sección `[maospix-local]` con `SigLevel = Optional TrustAll` y `Server = file:///home/maospy/maospix-kde/repo` (la ruta es absoluta: hay que cambiarla si se muda el proyecto).
- Los .pkg.tar.zst están en .gitignore: al mudar el proyecto hay que copiar `repo/` o reconstruir.

### 3.4 Calamares (instalador)
- Configuración en `airootfs/etc/calamares/`: `settings.conf` (secuencia de módulos), `modules/` (unpackfs, users, partition, shellprocess) y branding propio `maospix-kde` con el logo del gatito.
- `users.conf`: `allowWeakPasswords: true` y la casilla "contraseñas fuertes" desactivada por defecto.
- `partition.conf`: Btrfs por defecto, con selector (btrfs, ext4, xfs), y la partición EFI montada en `/boot` (ver problemas).
- `shellprocess@postinstall` ejecuta `/usr/local/bin/maospix-postinstall` dentro del sistema instalado: restaura el kernel, borra restos del live (autologin, sudoers del live, servicios), bloquea root, inicializa pacman-key, borra /home/liveuser, desinstala Calamares y se borra a sí mismo.
- `shellprocess@postboot` (después de instalar el bootloader) ejecuta `maospix-postboot`: si `/` es Btrfs, configura snapper y habilita snapper-cleanup.timer y grub-btrfsd, y regenera grub.cfg.

### 3.5 Identidad del sistema
- os-release y lsb-release con `ID=maospix-kde`, `ID_LIKE=arch`, `NAME="Maospix-KDE"`.
- Estos archivos chocan con los de paquetes de Arch. Solución: se guardan en `/usr/share/maospix/overrides/` y un hook de pacman (`maospix-overrides.hook`) los copia de nuevo tras cada instalación o actualización de filesystem, lsb-release, plasma-desktop, plasma-workspace y bash. NoExtract en pacman.conf no funcionó.

### 3.6 Tema y escritorio
- Look-and-feel propio `org.maospix.dark` con Nordic Darker, iconos Papirus-Dark, cursor Breeze y un script de layout (`contents/layouts/org.kde.plasma.desktop-layout.js`).
- Se aplica por `/etc/xdg/kdeglobals` (LookAndFeelPackage, navegador Brave, terminal maospix-terminal). GTK con Nordic-darker en `/etc/xdg/gtk-3.0` y `gtk-4.0`.
- Diseño: barra superior flotante (lanzador, clima, reloj, monitor de CPU/RAM, bandeja) y dock vertical a la izquierda con terminal, Dolphin, Brave, Discover, ajustes y un botón de apagado.
- Wallpapers propios (Maospix, Nord, Grafito, Negro), con la fuente Orbitron (licencia OFL). SDDM usa el gatito difuminado como fondo; el bloqueo de pantalla usa un fondo fijo.
- Los wallpapers se generan con `tools/gen-wallpapers.py` a partir de los originales de `assets/wallpapers-src/`. El texto se corrió a la derecha porque el dock lo tapaba en pantallas 16:10.

### 3.7 Terminal, shell y programas
- Terminal por defecto: Ghostty con tema Nord y JetBrains Mono (config en /etc/skel y en liveuser). `maospix-terminal` es un script que abre Ghostty y cae a Konsole si falla.
- fastfetch se ejecuta al abrir la terminal (override de /etc/bash.bashrc). Logo: el escudo de Maospix (diseño de Marcos), en `assets/logo/maospix-escudo.svg`; `tools/gen-ascii-logo.py` lo convierte en un logo de texto (estilo Arch, con el gatito dibujado a mano).
- Brave como navegador por defecto (Firefox quitado). cliamp como reproductor en terminal.
- paccache.timer limpia la caché de pacman cada semana.
- Maospix Hello: ventana de bienvenida en el primer inicio del sistema instalado (actualizar, tienda, instalar NVIDIA, configuración, sitio web, no mostrar más). La bienvenida de KDE queda oculta.
- `maospix-nvidia`: detecta la GPU NVIDIA e instala nvidia-open. No se preinstala para no romper nouveau en tarjetas viejas.

### 3.8 Btrfs, snapshots y zram
- Btrfs con subvolúmenes @, @home, @cache, @log y compresión zstd.
- snapper + snap-pac: snapshot antes y después de cada transacción de pacman. grub-btrfs agrega los snapshots al menú de GRUB.
- zram con zram-generator (mitad de la RAM, máximo 4 GB, zstd).
- Discover con Flatpak y Flathub preconfigurado.

## 4. Cómo se construye y se prueba

Dentro de tmux (para no perder el build si se corta SSH; salir con Ctrl+B y luego D, nunca Ctrl+C):

    tmux new -s build
    sudo rm -rf ~/archiso-work && sudo mkarchiso -v -w ~/archiso-work -o ~/maospix-kde/out ~/maospix-kde/archiso

El nombre de la ISO lleva la fecha del día. Copiar a Windows (PowerShell):

    scp maospy@192.168.100.72:maospix-kde/out/maospix-kde-AAAA.MM.DD-x86_64.iso C:\ISOs\

Capturas hacia el banco de trabajo:

    scp -r "C:\ISOs\carpeta" maospy@192.168.100.72:capturasN

VM de VirtualBox que funciona: Linux / Arch Linux 64-bit, EFI activado, 4 GB de RAM o más, 2 CPU, disco de 30 GB o más, controlador gráfico VMSVGA, memoria de vídeo 128 MB, sin aceleración 3D, dispositivo apuntador Tableta USB. Al terminar de instalar hay que quitar la ISO antes de reiniciar. La tecla Host es Ctrl derecho.

Avisos normales durante el build (no son errores graves): "Possibly missing firmware for module" y "binary not found: nbd-client" (módulo de arranque por red, que no usamos).

## 5. Historial de versiones

- ISO 1 y 2: perfil base y primeras pruebas de Calamares.
- ISO 3 a 5: tema, wallpapers, dock, barra superior.
- ISO 6: dock a la izquierda, Calamares y bienvenida en español, Ghostty como terminal, clima detectando Asunción.
- ISO 7: Btrfs con snapper, zram, Guest Additions, Discover + Flathub, Maospix Hello, helper NVIDIA. No arrancaba tras instalar.
- ISO 8: arregla el arranque (EFI en /boot). Probada completa con éxito.
- ISO 9: Hello oculto en el live.
- ISO 10: escudo en fastfetch y wallpapers, wallpapers con el texto libre del dock, fastfetch al abrir Ghostty.

## 6. Problemas encontrados y soluciones

| Problema | Causa | Solución |
|---|---|---|
| Archivos del sistema pisados por paquetes (os-release, layouts, bashrc) | Los paquetes reinstalan sus propios archivos | Hook de pacman que reaplica los overrides; NoExtract no funcionó |
| Konsole: no se pudo ocultar la barra de herramientas | El estado de la UI no se guarda en konsolerc ni kxmlgui | Se cambió a Ghostty |
| Ghostty no abre en VirtualBox ("OpenGL version is too old", requiere 4.3) | VirtualBox ofrece OpenGL 4.1 | Wrapper maospix-terminal: en VM usa renderizado por software (LIBGL_ALWAYS_SOFTWARE=1) y, si falla, cae a Konsole. En hardware real funciona directo |
| Brave: "no hay claves adecuadas para cifrar" | KWallet sin configurar | KWallet desactivado y --password-store=basic en brave-flags.conf |
| Cinco botones de sesión en el dock | Un launcher por acción | Un solo launcher maospix-power con el menú de salida de KDE |
| Portapapeles compartido de VirtualBox no funciona | Plasma 6.8 es solo Wayland y las Guest Additions no lo soportan | Sin solución (limitación de VirtualBox). La resolución sí se ajusta |
| Teclado y mouse congelados, loop en el live | Memoria de vídeo de la VM en 16 MB | Poner 128 MB y VMSVGA |
| Widget "Discos y dispositivos" se abre solo durante la instalación | KDE ve las particiones nuevas como discos conectados | Se deja (solo estético, solo en el live) |
| Maospix Hello aparecía en el live | El autostart usaba $USER | Se comprueba con `id -un` y con /run/archiso |
| No aparecía el selector de Btrfs en Calamares | Con un solo sistema de archivos disponible no se muestra | `availableFileSystemTypes` con btrfs, ext4 y xfs |
| El sistema instalado no arrancaba: "grub_cmd_linux: premature end of file /@/boot/vmlinuz-linux" | GRUB no pudo leer el kernel desde este Btrfs (el archivo estaba íntegro; se descartó la compresión zstd reescribiéndolo sin comprimir) | La partición EFI se monta en /boot (FAT32, 1 GB), así el kernel queda fuera de Btrfs. Limitación: los snapshots no incluyen el kernel |
| fastfetch no salía al abrir Ghostty | El script maospix-terminal suma un nivel de SHLVL y el bashrc exige SHLVL <= 1 | `export SHLVL=0` en maospix-terminal |
| Texto del wallpaper tapado por el dock | Pantalla 16:10 recorta los costados de una imagen 16:9 | Texto corrido unos 120 px a la derecha |
| Un corte de luz interrumpió un build | Energía | git e ISOs quedaron íntegros (git fsck OK); se repitió el build |
| Comando scp pegado dos veces en una línea | Error de copia | Copió dos veces; se borra el archivo sobrante |

## 7. Qué funciona (verificado en VirtualBox)

- Arranque del live en EFI, escritorio Plasma con tema Maospix, dock y barra.
- Instalador Calamares en español con selector de sistema de archivos.
- Sistema instalado: arranca, identidad Maospix-KDE, bienvenida en español, Calamares desinstalado, root bloqueado.
- Btrfs con compresión zstd, snapper y snap-pac (snapshots pre/post al instalar un paquete), entradas de snapshots en GRUB, zram, Flathub, Maospix Hello, botón de apagado, fastfetch, Guest Additions (resolución).
- Brave por defecto, Spotify instalable desde Discover, clima automático, esquinas redondeadas de los paneles.

## 8. Pendiente y próximos pasos

1. Subir el proyecto a GitHub (maospy): código sin los paquetes binarios, README, capturas y la ISO como release.
2. Probar en hardware real (pendrive con Ventoy): Ghostty directo, Wi-Fi, NVIDIA.
3. Ideas futuras: diseño alternativo "Islas", varios diseños elegibles desde Maospix Hello, versión maospix-ubuntu, zstd para builds de prueba.
4. Siguiente proyecto: Fedora o Arch + niri + dotfiles muy modernos (maospix-niri).
