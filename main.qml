import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.19 as Kirigami

Kirigami.ApplicationWindow {
    id: root
    width: 1000
    height: 700
    title: "NaviRust"

    // Isso garante que a janela use o blur e a decoração padrão do KWin
    background: Rectangle {
        color: Kirigami.Theme.backgroundColor
    }

    Kirigami.PageRouter {
        id: router
        initialRoute: "home"

        Kirigami.PageRoute {
            name: "home"
            Component {
                Kirigami.ScrollablePage {
                    title: "Biblioteca"

                    // Exemplo de Grid para álbuns
                    GridView {
                        id: albumGrid
                        anchors.fill: parent
                        cellWidth: 200; cellHeight: 250

                        // O modelo seria alimentado pelo Rust (qmetaobject)
                        model: albumModel

                        delegate: Item {
                            width: albumGrid.cellWidth
                            height: albumGrid.cellHeight

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: Kirigami.Units.smallSpacing

                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: width
                                    color: Kirigami.Theme.highlightColor // Placeholder da capa
                                }
                                Label {
                                    text: model.title
                                    font.bold: true
                                    elide: Text.ElideRight
                                    Layout.fillWidth: true
                                }
                                Label {
                                    text: model.artist
                                    opacity: 0.7
                                    elide: Text.ElideRight
                                    Layout.fillWidth: true
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
