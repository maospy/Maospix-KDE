import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation
{
    id: presentation

    Timer {
        interval: 6000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        Image {
            id: logo
            source: "maospix.png"
            width: 160; height: 160
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
        Text {
            anchors.horizontalCenter: logo.horizontalCenter
            anchors.top: logo.bottom
            anchors.topMargin: 20
            text: "<b>Bienvenido a Maospix-KDE</b><br/>Arch Linux + KDE Plasma, listo para usar."
            wrapMode: Text.WordWrap
            width: presentation.width
            horizontalAlignment: Text.AlignHCenter
        }
    }

    Slide {
        centeredText: "Hecho en Itauguá, Paraguay,<br/>por Marcos Olmedo (maospytek)."
    }

    Slide {
        centeredText: "Ya casi está.<br/>Estamos instalando tu sistema, esto puede tardar unos minutos."
    }

    function onActivate() { presentation.currentSlide = 0; }
    function onLeave() { }
}
