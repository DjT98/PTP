import os
project_path = os.path.abspath('') 
os.chdir(project_path)
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from ui_plm import Ui_MainWindow
from bpm_detection import read_wav, bpm_detector



Form, Window = uic.loadUiType("plm.ui")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.bpm_list = []

        self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)

        self.add_audio_files_to_scroll_area()

        # Get a list of all the audio files in the directory
        
    def add_audio_files_to_scroll_area(self):
        self.audio_dir = "Songs"
        audio_files = [
            os.path.join(file)
            for file in os.listdir(self.audio_dir)
            if file.endswith(".wav")  # Add more extensions if needed
        ]

        layout = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)

        # Add each audio file to the scrollable widget
        for file in audio_files:
            label = QLabel(parent=self.ui.scrollAreaWidgetContents)
            pixmap = QPixmap("Images/music_note.png")
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setText(file)
            layout.addWidget(label)

    def on_pushButton_clicked(self):

        self.ui.pushButton.clicked.disconnect()

        self.bpm_list = []  # Reset the list of beats per minute for each audio file
        audio_files = []
        for file in os.listdir(self.audio_dir):
            if file.endswith(".wav"):
                # Read the audio data from the file
                filepath = os.path.join(self.audio_dir, file)
                data, fs = read_wav(filepath)

                # Calculate the beats per minute for the audio data
                bpm, _ = bpm_detector(data, fs)

                # Add the beats per minute to the list
                self.bpm_list.append(bpm)
                audio_files.append(file)

        sorted_files = [file for _, file in sorted(zip(self.bpm_list, audio_files))]

        # Display the beats per minute for each audio file
        if len(self.bpm_list) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", "No audio files found in directory. Add .wav files to the Songs directory.")
        else:
            bpm_text = "\n".join([f"{file}: {float(bpm):.2f} bpm" for file, bpm in zip(os.listdir(self.audio_dir), self.bpm_list)])
            QtWidgets.QMessageBox.information(self, "BPM Results", bpm_text)

            with open("sorted_by_bpm.txt", "w") as f:
                      f.write("\n".join(sorted_files))

        self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)
    

if __name__ == "__main__":
   app = QApplication([])
   window = MainWindow()
   window.show()
   app.exec()