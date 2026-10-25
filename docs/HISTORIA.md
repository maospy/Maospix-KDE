# Maospix-KDE: historia de construcción paso a paso

Autor: Marcos Olmedo (maospytek), Itauguá, Paraguay. Base: Arch Linux + KDE Plasma, construida con archiso e instalador gráfico Calamares. Documento escrito el 24/10/2026, durante la ISO 7.

## 1. Idea y reglas del proyecto

- Distro propia, parte de la familia maospix (antes: maospix-bspwm sobre Fedora y maospy-hypr sobre Arch + Hyprland).
- Estilo Xero Linux / Garuda: todo preinstalado y tematizado, con instalador gráfico.
- Todos los proyectos nuevos se llaman maospix-*.
- Se trabaja de a un paso: se prueba el comando, se confirma el resultado y recién se sigue.

## 2. Entorno de trabajo

- Banco de trabajo: una PC con Arch Linux minimal (usuario maospy, carpeta ~/maospix-kde), accesible por SSH desde Windows. Tiene 2 núcleos, un HDD y 7,6 GB de RAM.
- Regla: no instalar la ISO en el disco de esta máquina. Un SSD M.2 con Omarchy instalado no se toca.
- Las pruebas se hacen en VirtualBox en Windows (ISO en C:\ISOs\, EFI activado).
- Los builds son lentos (varios minutos) por la compresión xz, los 2 núcleos y el HDD. Para pruebas se puede usar zstd.

## 3. Paso a paso de la construcción

### 3.1 Perfil archiso
1. Se copió el perfil "releng" de archiso a ~/maospix-kde/archiso.
2. En profiledef.sh: iso_name=maospix-kde, y la tabla file_permissions con los archivos que necesitan permisos (carpeta de liveuser, scripts de /usr/local/bin, etc.).
3. Se definió la lista de paquetes en packages.x86_64: KDE Plasma, SDDM, Calamares, Brave, Ghostty, Konsole, fastfetch, Papirus, Discover, flatpak, etc.

### 3.2 Repositorio local para paquetes AUR
- archiso no puede usar AUR directamente. Se construyeron los paquetes con makepkg y se guardaron en ~/maospix-kde/repo, declarado como [maospix-local] en archiso/pacman.conf.
- Paquetes propios: calamares 3.4.2, brave-bin, cliamp-bin. Los PKGBUILD están en ~/maospix-kde/pkgbuilds/.
- Los .pkg.tar.zst están en .gitignore: al mudar el proyecto hay que copiar la carpeta repo/ o reconstruir.

### 3.3 Calamares (instalador)
- Configuración en airootfs/etc/calamares/: settings.conf, modules/ (unpackfs, users, partition, shellprocess) y branding propio "maospix-kde" con el logo del gatito.
- users.conf: allowWeakPasswords en true y la casilla "contraseñas fuertes" desactivada por defecto.
- Script maospix-postinstall (corre dentro del sistema instalado): restaura el kernel, borra restos del live (autologin, sudoers del live, servicios), bloquea root, inicializa pacman-key, borra /home/liveuser, desinstala Calamares y se borra a sí mismo.

### 3.4 Identidad del sistema
- os-release y lsb-release con ID=maospix-kde, ID_LIKE=arch, NAME "Maospix-KDE".
- Estos archivos chocan con los de paquetes de Arch. Solución: se guardan en /usr/share/maospix/overrides/ y un hook de pacman (maospix-overrides.hook) los copia de nuevo tras cada instalación o actualización de filesystem, lsb-release, plasma-desktop, plasma-workspace y bash.
- Se probó NoExtract en pacman.conf y no funcionó; el hook sí.

### 3.5 Tema y escritorio
- Look-and-feel propio org.maospix.dark con Nordic Darker, iconos Papirus-Dark y cursor Breeze.
- Esquema de color NordicDarker, tema GTK Nordic-darker, configuración en /etc/xdg/kdeglobals.
- Diseño: barra superior flotante (lanzador, clima, reloj, monitor de CPU/RAM, bandeja) y dock vertical a la izquierda, flotante, con terminal, Dolphin, Brave, Discover, ajustes y botón de apagado.
- Se generaron wallpapers propios con Python (PIL) y la fuente Orbitron (licencia OFL): Maospix, Maospix-Nord, Maospix-Grafito, Maospix-Negro.
- SDDM usa el gatito difuminado como fondo; el bloqueo de pantalla usa un fondo fijo.

### 3.6 Terminal, shell y programas
- Terminal por defecto: Ghostty con tema Nord y JetBrains Mono (config en /etc/skel y en liveuser). fastfetch se ejecuta al abrir la terminal, con un logo propio del gatito en caracteres de colores.
- Brave como navegador por defecto (Firefox quitado). cliamp como reproductor de música en terminal.
- paccache.timer para limpiar la caché de pacman cada semana.
- Maospix Hello: ventana de bienvenida en el primer inicio (actualizar, tienda, NVIDIA, configuración, sitio, no mostrar más). La bienvenida de KDE queda oculta.
- maospix-nvidia: ayudante que detecta la GPU NVIDIA e instala nvidia-open. No se preinstala para no romper nouveau en tarjetas viejas.

### 3.7 Btrfs, snapshots y zram (ISO 7)
- Calamares con Btrfs por defecto (subvolúmenes @, @home, @cache, @log, compresión zstd).
- snapper + snap-pac + grub-btrfs: snapshots antes y después de cada transacción de pacman y entradas en el menú de GRUB. Se configuran con el script maospix-postboot al final de la instalación.
- zram con zram-generator (mitad de la RAM, máximo 4 GB, zstd).
- Discover con Flatpak y Flathub preconfigurado.

## 4. Cómo se construye y se prueba

Dentro de tmux (para no perder el build si se corta SSH; salir con Ctrl+B y luego D, nunca Ctrl+C):

    tmux new -s build
    sudo rm -rf ~/archiso-work && sudo mkarchiso -v -w ~/archiso-work -o ~/maospix-kde/out ~/maospix-kde/archiso

Copiar la ISO a Windows (PowerShell):

    scp maospy@192.168.100.72:maospix-kde/out/maospix-kde-2026.10.24-x86_64.iso C:\ISOs\

Capturas de pantalla hacia el banco de trabajo:

    scp -r "C:\ISOs\carpeta" maospy@192.168.100.72:capturasN

Configuración de la VM de VirtualBox que funciona: Linux / Arch Linux 64-bit, EFI activado, 4 GB de RAM o más, 2 CPU, disco de 30 GB, controlador gráfico VMSVGA, memoria de vídeo 128 MB, sin aceleración 3D, dispositivo apuntador Tableta USB. Al terminar de instalar hay que quitar la ISO antes de reiniciar. La tecla Host es Ctrl derecho.

## 5. Historial de versiones

- ISO 1 y 2: perfil base y primeras pruebas de Calamares.
- ISO 3 a 5: tema, wallpapers, dock, barra superior. La ISO 4 fue calificada como "lo mejor que he visto".
- ISO 6: dock a la izquierda, Calamares y bienvenida de KDE en español, Ghostty como terminal, clima detectando Asunción.
- ISO 7: Btrfs con snapper, zram, Guest Additions, Discover + Flathub, Maospix Hello, logo fastfetch, helper NVIDIA.

## 6. Problemas encontrados y soluciones

| Problema | Causa | Solución |
|---|---|---|
| Archivos del sistema pisados por paquetes (os-release, layouts, bashrc) | Los paquetes reinstalan sus propios archivos | Hook de pacman que reaplica los overrides; NoExtract no funcionó |
| Konsole: no se pudo ocultar la barra de herramientas | El estado de la UI no se guarda en konsolerc ni kxmlgui | Se cambió a Ghostty como terminal |
| Ghostty no abre en VirtualBox ("OpenGL version is too old", requiere 4.3) | VirtualBox ofrece OpenGL 4.1 | Wrapper maospix-terminal: en VM usa renderizado por software (LIBGL_ALWAYS_SOFTWARE=1) y si falla en 5 s cae a Konsole. En hardware real funciona directo |
| Brave: "no hay claves adecuadas para cifrar" | KWallet sin configurar | KWallet desactivado y --password-store=basic en brave-flags.conf |
| Cinco botones de sesión en el dock | Un launcher por acción | Un solo launcher maospix-power con el menú de salida de KDE |
| Portapapeles compartido de VirtualBox no funciona | Plasma 6.8 es solo Wayland y las Guest Additions no lo soportan | Sin solución; es limitación de VirtualBox. La resolución sí se ajusta |
| Teclado y mouse congelados, loop en el live (ISO 7) | Memoria de vídeo de la VM en 16 MB | Poner 128 MB y VMSVGA |
| Widget "Discos y dispositivos" se abre solo durante la instalación | KDE ve las particiones nuevas como discos conectados | Pendiente: ocultarlo en el live (solo estético) |
| Maospix Hello aparece también en el live | Autostart no excluido para liveuser | Pendiente de corregir |
| No aparecía la opción de elegir Btrfs en Calamares | Con un solo sistema de archivos disponible no se muestra el selector | availableFileSystemTypes con btrfs, ext4 y xfs |
| El sistema instalado no arranca: "grub_cmd_linux: premature end of file /@/boot/vmlinuz-linux" | GRUB no puede leer el kernel desde este Btrfs (el archivo estaba íntegro; se descartó la compresión zstd reescribiéndolo sin comprimir) | La partición EFI se monta en /boot (FAT32, 1 GB) para que el kernel quede fuera de Btrfs. Verificado: la ISO 8 arranca y funciona completa |
| Un corte de luz interrumpió un build | Energía | git e ISOs quedaron íntegros (git fsck OK); se repitió el build |
| Comando scp pegado dos veces en una línea | Error de copia | Copió dos veces; se borra el archivo sobrante |

## 7. Qué funciona (verificado en VirtualBox)

- Arranque del live en EFI, escritorio Plasma con tema Maospix, dock y barra.
- Instalador Calamares en español, con la casilla de contraseñas débiles.
- Sistema instalado: identidad Maospix-KDE, bienvenida en español, Calamares desinstalado, root bloqueado.
- Brave por defecto, clima automático (Asunción), esquinas redondeadas de los paneles, fastfetch al abrir terminal.
- Btrfs se crea bien en el disco y zram funciona en el live.

## 8. Pendiente

1. ISO 9: build final con Hello oculto en el live (la ISO 8 ya fue verificada: arranque, Btrfs, snapper, snap-pac, grub-btrfs, zram, Flathub).
2. Ocultar el widget de dispositivos en el live y no mostrar Maospix Hello en el live.
3. Probar Ghostty en hardware real, Discover/Flathub y el botón de apagado.
4. Si queda satisfecho: probar en un pendrive (Ventoy), escribir README, capturas, subir a GitHub (maospy) y publicar un release.
5. Ideas futuras: diseño alternativo "Islas" (paneles superiores en islas más dock vertical translúcido), varios diseños elegibles desde Maospix Hello, versión maospix-ubuntu separada, zstd para builds de prueba.
