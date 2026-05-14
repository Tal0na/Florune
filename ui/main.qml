import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import org.kde.kirigami 2.20 as Kirigami

import Florune 1.0

Kirigami.ApplicationWindow {

    id: root

    width: 1200
    height: 800

    visible: true

    title: "Florune"

    color: "#111111"

    FloruneEngine {
        id: florune_engine
    }

    Component.onCompleted: {
        florune_engine.fetch_albums()
    }

    pageStack.initialPage: Kirigami.ScrollablePage {

        title: "Biblioteca"

        ColumnLayout {

            anchors.fill: parent
            anchors.margins: 24

            spacing: 20

            Rectangle {

                Layout.fillWidth: true
                Layout.preferredHeight: 80

                radius: 16

                color: "#1b1b1b"

                border.color: "#2b2b2b"

                RowLayout {

                    anchors.fill: parent
                    anchors.margins: 20

                    spacing: 20

                    ColumnLayout {

                        Layout.fillWidth: true

                        spacing: 4

                        Text {

                            text: "Florune"

                            color: "white"

                            font.pixelSize: 28
                            font.bold: true
                        }

                        Text {

                            text:
                                florune_engine.status

                            color: "#aaaaaa"

                            font.pixelSize: 14
                        }
                    }

                    Button {

                        text: "Atualizar"

                        onClicked: {
                            florune_engine.fetch_albums()
                        }
                    }
                }
            }

            GridView {

                id: albumGrid

                Layout.fillWidth: true
                Layout.fillHeight: true

                cellWidth: 220
                cellHeight: 320

                clip: true

                model:
                    florune_engine.album_model

                delegate: Item {

                    width: 200
                    height: 300

                    Rectangle {

                        id: card

                        anchors.fill: parent

                        radius: 18

                        color: "#1d1d1d"

                        border.width: 1
                        border.color: "#2b2b2b"

                        Behavior on scale {
                            NumberAnimation {
                                duration: 120
                            }
                        }

                        MouseArea {

                            anchors.fill: parent

                            hoverEnabled: true

                            onEntered: {
                                card.scale = 1.03
                            }

                            onExited: {
                                card.scale = 1.0
                            }

                            onClicked: {
                                console.log(
                                    title
                                )
                            }
                        }

                        Column {

                            anchors.fill: parent
                            anchors.margins: 12

                            spacing: 12

                            Rectangle {

                                width: parent.width
                                height: 190

                                radius: 14

                                clip: true

                                color: "#2a2a2a"

                                Image {

                                    anchors.fill: parent

                                    source:
                                        florune_engine.get_cover_url(
                                            albumId
                                        )

                                    fillMode:
                                        Image.PreserveAspectCrop

                                    asynchronous: true

                                    cache: true
                                }
                            }

                            Column {

                                width: parent.width

                                spacing: 4

                                Text {

                                    width: parent.width

                                    text: title

                                    color: "white"

                                    font.pixelSize: 16
                                    font.bold: true

                                    elide:
                                        Text.ElideRight
                                }

                                Text {

                                    width: parent.width

                                    text: artist

                                    color: "#9a9a9a"

                                    font.pixelSize: 13

                                    elide:
                                        Text.ElideRight
                                }
                            }
                        }
                    }
                }

                ScrollBar.vertical: ScrollBar {

                    policy:
                        ScrollBar.AsNeeded
                }
            }
        }
    }
}
