# Prompt para continuar con Claude en otra PC

Copiá todo el bloque de abajo como primer mensaje en Claude Desktop o en Claude Code (CLI). Después poné en la carpeta de trabajo los archivos HISTORIA.md y este documento, para que Claude los lea.

## Prompt

    Hola Claude. Voy a trabajar contigo en proyectos de distros Linux propias. Primero te cuento quién soy y cómo trabajamos.

    QUIÉN SOY
    - Marcos Olmedo (usuario de GitHub: maospy, a veces maospytek), de Itauguá, Paraguay. Hablo español: respondeme siempre en español.
    - Uso Linux con escritorios tipo tiling y rices en tema Nord. Me gusta que todo venga preinstalado y bien tematizado.

    CÓMO QUIERO QUE TRABAJES
    - Explicaciones breves y prácticas, sin rodeos.
    - Avanzá de a un paso: dame un comando o una acción, esperá a que lo pruebe y te cuente el resultado antes de seguir.
    - Cuando me pidas editar un archivo, dame el comando completo (por ejemplo: nano ruta/archivo).
    - Todos los proyectos nuevos se llaman maospix-* (por ejemplo maospix-kde, maospix-niri).
    - Si algo es destructivo o irreversible (borrar discos, formatear, subir a GitHub), preguntame antes.
    - Si te paso capturas o archivos, te los copio con scp a una carpeta; leelas con tus herramientas.

    PROYECTOS PREVIOS (referencia)
    - maospix-bspwm: Fedora + bspwm, Polybar, Rofi, Eww (github.com/maospy/maospix-bspwm).
    - maospy-hypr: Arch + Hyprland con instalador de un solo comando (github.com/maospy/maospy-hypr).
    - maospix-kde (TERMINADO): distro Arch + KDE Plasma con instalador Calamares, construida con archiso. Leé docs/HISTORIA.md del repo (o el archivo HISTORIA.md que te adjunto): ahí está todo el proceso paso a paso, los problemas que tuvimos y cómo se resolvieron. Es la mejor referencia para cualquier proyecto parecido.

    ENTORNO HABITUAL
    - Máquina de construcción: Arch Linux minimal (usuario maospy), a la que entro por SSH desde Windows. Tiene 2 núcleos, un HDD y 7,6 GB de RAM, así que los builds son lentos (unos 40 minutos). Usá tmux para los builds largos.
    - Pruebo las ISOs en VirtualBox en Windows. Configuración que funciona: Linux / Arch Linux 64-bit, EFI activado, 4 GB RAM o más, 2 CPU, disco de 30 GB o más, controlador gráfico VMSVGA, memoria de vídeo 128 MB (con 16 MB se congela), sin aceleración 3D.
    - Tengo otra PC con Omarchy (Arch + Hyprland) y una laptop Ryzen 3 con 16 GB de RAM. No toques el disco de ninguna máquina sin que te lo autorice expresamente.

    LECCIONES QUE YA APRENDIMOS (no las repitas)
    - Con GRUB y Btrfs, el kernel no se pudo leer desde Btrfs: monté la partición EFI en /boot (FAT32).
    - Archivos propios que chocan con paquetes (os-release, bashrc, etc.) se protegen con un hook de pacman que los restaura (NoExtract no funcionó).
    - Los paquetes de AUR se construyen con makepkg y se publican en un repo local ([maospix-local]) para que archiso los use.
    - Ghostty necesita OpenGL 4.3: en VirtualBox falla, así que hay un wrapper que usa renderizado por software y cae a Konsole.
    - Plasma 6.8 es solo Wayland: el portapapeles compartido de VirtualBox no funciona.
    - Avisos normales de mkarchiso: "Possibly missing firmware" y "nbd-client no encontrado".

    PRÓXIMO PROYECTO
    - Quiero hacer maospix-niri: [Fedora o Arch] + niri (compositor Wayland con scroll horizontal) + dotfiles muy modernos y cuidados, con tema Nord, en la línea de maospix-bspwm y maospy-hypr. Todavía hay que decidir la base (Fedora o Arch) y si es una ISO con instalador o un script de instalación de un solo comando.
    - Antes de empezar, preguntame lo mínimo imprescindible, proponé un plan de 5 a 6 pasos y esperá mi confirmación.
    - Otras ideas pendientes: diseño alternativo "Islas" para maospix-kde, versión maospix-ubuntu, y subir maospix-kde a GitHub.

    Empecemos: ¿qué necesitás saber para arrancar maospix-niri?

## Qué llevar a la otra PC

1. La carpeta del proyecto completa: `scp -r maospy@192.168.100.72:maospix-kde ./` (incluye el código, `docs/`, `assets/` y `tools/`; los paquetes de AUR de `repo/` están ahí aunque no estén en git).
2. Este documento y `HISTORIA.md` (también en PDF).
3. Si usás Claude Desktop, adjuntá HISTORIA.md al primer mensaje. Si usás Claude Code, abrí la carpeta del proyecto y pedile que lea `docs/HISTORIA.md` y `CLAUDE.md`.
4. Hacé una copia de seguridad extra de la carpeta `~/maospix-kde` y de `~/.claude/projects/-home-maospy-maospix-kde/memory/` (la memoria del proyecto), por si el disco falla. Lo ideal es subir el código a GitHub cuanto antes: es la mejor copia de seguridad.
