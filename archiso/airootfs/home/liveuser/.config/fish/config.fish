# Maospix-KDE: sin saludo de fish, fastfetch al abrir una terminal
set -g fish_greeting

if status is-interactive; and test "$SHLVL" -le 1; and command -q fastfetch
    fastfetch
end
