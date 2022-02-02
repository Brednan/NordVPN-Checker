import QtQuick
import QtQuick.Controls
import GUI_Test

Rectangle {
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Text {
        text: qsTr("Hello GUI_Test")
        anchors.centerIn: parent
        font.family: Constants.font.family
    }
}
