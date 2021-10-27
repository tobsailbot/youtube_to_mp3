from __future__ import unicode_literals
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QInputDialog
from youtube_mp3_ui import Ui_MainWindow  # importing our generated file
import sys
import os
import youtube_dl



# opciones de formato y directorio de destino
ydl_opts = {'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],'outtmpl': '%(title)s.%(ext)s'}



class mywindow(QtWidgets.QMainWindow):

    def __init__(self):  
         
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
    
        self.ui.setupUi(self)
    
        self.ui.pushButton_2.clicked.connect(self.btnClicked) # al hacer click en pushButton_2 se activa la funcion btnClicked

        self.ui.pushButton_4.clicked.connect(self.btn4Clicked)

        # intentar leer archivo 'save_folder.txt' y mostrarlo como 'current folder:', except si este no existe imprimir 'Select folder first...' 
        
        try:
                f = open("save_folder.txt", "r")
                current_folder = f.read()
                self.ui.plainTextEdit.setPlainText("Current folder: "+current_folder)
        except FileNotFoundError:
                self.ui.plainTextEdit.setPlainText('Select folder first...')
 


    def btnClicked(self): #al clickear el boton lee el texto del lineEdit, lo pasa a una variable, y descarga el video

            try:
                    video_url = self.ui.lineEdit.text()
                    print("LA URL DEL VIDEO ES: "+video_url)
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([video_url])
                            self.ui.plainTextEdit.setPlainText('Download finished ..')
        # si aparece cualquier tipo de error mostrar el msj en pantalla
            except:
                    self.ui.plainTextEdit.setPlainText('Error, check the URL and remember to install ffmpeg  ..')
                

    def btn4Clicked(self): # boton set folder

        # abrir ventana para seleccionar un directorio, se establece titulo de la ventana y se abre al comienzo c:// 
        dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select save folder:', 'c:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        # crea un archivo y lo sobreescribe
        f = open("save_folder.txt", "w")
        # escribe el directorio seleccionado dentro del archivo
        f.write(dir_)
        # abre el archivo en modo read
        f = open("save_folder.txt", "r")
        # asigna la string a una variable 'folder_name'
        folder_name = f.read()
        # si el archivo esta vacio, pedir seleccionar carpeta..
        filesize = os.path.getsize("save_folder.txt")
        if filesize <= 0:
                self.ui.plainTextEdit.setPlainText('Select folder first...')
        # se establece el directorio seleccionado como la ruta de destino de nuestro archivo
        else:
                self.ui.plainTextEdit.setPlainText("Current folder: "+folder_name)
                ydl_opts['outtmpl'] = folder_name+'/'+'%(title)s.%(ext)s'
        f.close()
        

app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())


