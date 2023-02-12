import serial
from time import time, ctime
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
import os

ser = serial.Serial('COM3')
ser.flushInput()

plot_window = 50
y_var_pressure = np.array(np.zeros([plot_window]))
y_var_breathe = np.array(np.zeros([plot_window]))
y_var_solenoids = np.array(np.zeros([plot_window]))

plt.ion()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
line_breathe, = ax1.plot(y_var_breathe)
line_solenoids, = ax2.plot(y_var_solenoids)
line_pressure, = ax3.plot(y_var_pressure)


def uniquify(path): # iterates file name
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

# iterates file name
file_name = uniquify("test_data.csv")

while True:
    try:
        serial_data = ser.readline()
        try:
            # decoded_bytes = float(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
            decoded_string_data = str(serial_data[0:len(serial_data) - 2].decode("utf-8"))
            string_array = decoded_string_data.split(' ')
            number_array = [int(numeric_string) for numeric_string in string_array]

            breathe = number_array[0]
            pressure = number_array[1]
            solenoids = number_array[2]

            print(breathe, pressure, solenoids)

        except:
            continue
        with open(file_name, "a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([time(), breathe, pressure, solenoids])

    # Plotting Breathe
        y_var_breathe = np.append(y_var_breathe, breathe)
        y_var_pressure = np.append(y_var_pressure, pressure)
        y_var_solenoids = np.append(y_var_solenoids, solenoids)

        y_var_breathe = y_var_breathe[1:plot_window + 1]
        line_breathe.set_ydata(y_var_breathe)
        y_var_pressure = y_var_pressure[1:plot_window + 1]
        line_pressure.set_ydata(y_var_pressure)
        y_var_solenoids = y_var_solenoids[1:plot_window + 1]
        line_solenoids.set_ydata(y_var_solenoids)
        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()
        ax3.relim()
        ax3.autoscale_view()
        ax3.relim()
    # Draw Plot
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        print("Keyboard Interrupt")
        break






# #!/usr/bin/python3
# # -*-coding:Utf-8 -*
#
# import sys, os, time
# import platform
# from random import randint
# import serial, serial.tools.list_ports
#
# # interface import
# import PySide2
#
# from PySide2.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QTextEdit, QLineEdit, QPushButton, QMessageBox, \
#     QWidget, QGridLayout, QTextEdit, QGroupBox, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
#
# from PySide2.QtGui import QIcon, QScreen
#
# __prgm__ = 'Serial Monitor'
# __version__ = '0.0.2'
#
#
# def find_USB_device(USB_DEV_NAME=None):
#     myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
#     print(myports)
#     usb_port_list = [p[0] for p in myports]
#     usb_device_list = [p[1] for p in myports]
#     print(usb_device_list)
#
#     if USB_DEV_NAME is None:
#         return myports
#     else:
#         USB_DEV_NAME = str(USB_DEV_NAME).replace("'", "").replace("b", "")
#         for device in usb_device_list:
#             print("{} -> {}".format(USB_DEV_NAME, device))
#             print(USB_DEV_NAME in device)
#             if USB_DEV_NAME in device:
#                 print(device)
#                 usb_id = device[device.index("COM"):device.index("COM") + 4]
#
#                 print("{} port is {}".format(USB_DEV_NAME, usb_id))
#                 return usb_id
#
#
# class GroupClass(QGroupBox):
#     def __init__(self, widget, title="Connection Configuration"):
#         super().__init__(widget)
#         self.widget = widget
#         self.title = title
#         self.sep = "-"
#         self.id = -1
#         self.name = ''
#         self.portlist = find_USB_device()
#         self.items = [p[0] for p in self.portlist]  # ["COM1","COM2"]
#         self.serial = None
#         # self.motionDict={"POSITION BASED":" Describe motion based on position","VELOCITY BASED":" Describe motion based on velocity", "LOOP":" Describe loop motion", "PINGPONG":" Describe pingpong motion", "INTERACTIF":" Describe interactive motion"}
#         self.init()
#
#     def init(self):
#         self.setTitle(self.title)
#
#         self.selectlbl = QLabel("Select port:")
#         # label
#         self.typeBox = QComboBox()
#         self.typeBox.addItems(self.items)  # database getMotionType()
#         self.typeBox.setCurrentIndex(self.typeBox.count() - 1)
#
#         # btn
#         button = QPushButton("Connect")
#         button.clicked.connect(self.connect)
#         # hbox.addWidget(button)
#         sendBtn = QPushButton("send")
#         sendBtn.clicked.connect(self.sendData)
#         # hbox.addWidget(button)
#
#         titlelbl = QLabel("Enter")
#         self.title = QLineEdit("")
#         desclbl = QLabel("Console")
#         self.desc = QTextEdit("")
#
#         # self.add=QPushButton("Ajouter/Modifier")
#         # self.add.clicked.connect(self.addItem)
#         # self.rem=QPushButton("Supprimer")
#         # self.rem.clicked.connect(self.remItem)
#
#         self.fields = QGridLayout()
#         self.fields.addWidget(self.selectlbl, 0, 0, 1, 1)
#         self.fields.addWidget(self.typeBox, 0, 1, 1, 1)
#         self.fields.addWidget(button, 0, 2, 1, 1)
#
#         self.fields.addWidget(titlelbl, 1, 0, 1, 1)
#         self.fields.addWidget(self.title, 1, 1, 1, 1)
#         self.fields.addWidget(sendBtn, 1, 2, 1, 1)
#         self.fields.addWidget(desclbl, 2, 0, 1, 1)
#         self.fields.addWidget(self.desc, 3, 1, 1, 1)
#         # self.fields.addWidget(self.add,2,2,1,1)
#         # self.fields.addWidget(self.rem,3,2,1,1)
#         self.setLayout(self.fields)
#
#     def connect(self):
#
#         self.desc.setText("")
#         self.desc.setText(">> trying to connect to port %s ..." % self.typeBox.currentText())
#         # with serial.Serial(self.typeBox.currentText(), 115200, timeout=1) as self.serial:
#         if self.serial is None:
#             self.serial = serial.Serial(self.typeBox.currentText(), 115200, timeout=1)
#             time.sleep(0.05)
#             # self.serial.write(b'hello')
#             answer = self.readData()
#             if answer != "":
#                 self.desc.setText(self.desc.toPlainText() + "\n>> Connected!\n" + answer)
#         else:
#             self.desc.setText(">> {} already Opened!\n".format(self.typeBox.currentText()))
#
#     def sendData(self):
#         if self.serial.isOpen():
#             if self.title.text() != "":
#                 self.serial.write(self.title.text().encode())
#                 answer = self.readData()
#                 if (self.title.text().encode() == "scan"):
#                     print("scanning results -> " + answer.find("0x"))
#                 else:
#                     print(answer.find("0x"))
#                 self.desc.setText(self.desc.toPlainText() + "\n" + answer)
#
#     def readData(self):
#         # self.serial.flush() # it is buffering. required to get the data out *now*
#         answer = ""
#         while self.serial.inWaiting() > 0:  # self.serial.readable() and
#
#             print(self.serial.inWaiting())
#             answer += "\n" + str(self.serial.readline()).replace("\\r", "").replace("\\n", "").replace("'", "").replace(
#                 "b", "")
#             # print(self.serial.inWaiting())
#         # self.desc.setText(self.desc.toPlainText()+"\n"+answer)
#         return answer
#
#
# class SerialInterface(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.width = 650
#         self.height = 350
#
#         self.resize(self.width, self.height)
#         self.setWindowIcon(QIcon('./resources/logo-100.png'))
#         self.setWindowTitle(__prgm__)
#
#         # center window on screen
#         qr = self.frameGeometry()
#         cp = QScreen().availableGeometry().center()
#         qr.moveCenter(cp)
#
#         # init layout
#         centralwidget = QWidget(self)
#         centralLayout = QHBoxLayout(centralwidget)
#         self.setCentralWidget(centralwidget)
#
#         # add connect group
#         self.connectgrp = GroupClass(self)
#         centralLayout.addWidget(self.connectgrp)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     frame = SerialInterface()
#     frame.show()
#     sys.exit(app.exec_())