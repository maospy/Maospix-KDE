// Maospix Dark: barra superior fina + dock flotante abajo

var desktopsArray = desktopsForActivity(currentActivity());
for (var j = 0; j < desktopsArray.length; j++) {
    desktopsArray[j].wallpaperPlugin = 'org.kde.image';
    desktopsArray[j].currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    desktopsArray[j].writeConfig("Image", "file:///usr/share/wallpapers/Maospix");
}

// --- Barra superior ---
var top = new Panel;
top.location = "top";
top.height = 2 * Math.ceil(gridUnit * 1.2 / 2);
top.floating = true;
top.opacity = "translucent";
top.addWidget("org.kde.plasma.kickoff");
top.addWidget("org.kde.plasma.panelspacer");
var weather = top.addWidget("org.kde.plasma.weather");
weather.currentConfigGroup = ["General"];
weather.writeConfig("showTemperatureInCompactMode", true);
weather.writeConfig("showTemperatureInTooltip", true);
var clock = top.addWidget("org.kde.plasma.digitalclock");
clock.currentConfigGroup = ["Appearance"];
clock.writeConfig("showDate", false);
top.addWidget("org.kde.plasma.panelspacer");
top.addWidget("org.kde.plasma.systemmonitor.cpucore");
top.addWidget("org.kde.plasma.systemmonitor.memory");
top.addWidget("org.kde.plasma.systemtray");

// --- Dock flotante ---
var dock = new Panel;
dock.location = "left";
dock.height = 2 * Math.ceil(gridUnit * 2.2 / 2);
dock.floating = true;
dock.opacity = "translucent";
dock.alignment = "center";
dock.lengthMode = "fit";
var tasks = dock.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", [
    "applications:maospix-terminal.desktop",
    "applications:org.kde.dolphin.desktop",
    "applications:brave-browser.desktop",
    "applications:systemsettings.desktop",
    "applications:maospix-power.desktop"
]);
dock.addWidget("org.kde.plasma.marginsseparator");
dock.addWidget("org.kde.plasma.trash");
