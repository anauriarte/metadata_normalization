import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QGridLayout, QHeaderView

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt

from normalize_metadata import *
from PyQt5 import QtGui, QtCore
import sys
import os
from stat import ST_MTIME
import os, sys, time, subprocess

class FileDialog(QMainWindow):
    def __init__(self, parent=None):
        super(FileDialog, self).__init__(parent)

    def openInputFileNameDialog(self, main_w):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Browse File", "","Zip files (*.zip)", options=options)
        if fileName:
            print(fileName)
            main_w.metadata_directory = fileName
            main_w.inputFile.setText(fileName)
            self.close()

    def openOuputDirDialog(self, main_w):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        dir = QFileDialog.getExistingDirectory(self, "", "", options=options)
        if dir:
            print(dir)
            main_w.outdir = dir
            main_w.outputDir.setText(dir)
            self.close()


class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 1000
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.showMaximized()

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.dict_fields_added = {}
        #Select metadata file label
        self.l1 = QLabel(self)
        self.l1.setGeometry(10, 10, 200, 16)
        self.l1.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.l1.setText("Select metadata zip file")

        #Button to browse metadata file
        self.pushButton_input = QPushButton('Browse File', self)
        self.pushButton_input.setStyleSheet('QPushButton {color: #004080; font-family:Arial ;}')
        self.pushButton_input.move(10, 30)

        #Field with file name
        self.inputFile = QTextEdit(self)
        self.inputFile.setGeometry(120, 35, 500, 16)

        #Select output dir
        self.l2 = QLabel(self)
        self.l2.setGeometry(10, 60, 200, 16)
        self.l2.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.l2.setText("Select output directory")

        #Button to browse output dir
        self.pushButton_output = QPushButton('Browse Dir', self)
        self.pushButton_output.setStyleSheet('QPushButton {color: #004080; font-family:Arial}')
        self.pushButton_output.move(10, 80)

        #Field with output dir
        self.outputDir = QTextEdit(self)
        self.outputDir.setGeometry(120, 85, 500, 16)

        #Button to start normalization
        self.l3 = QLabel(self)
        self.l3.setGeometry(10, 120, 500, 16)
        self.l3.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.l3.setText("Press 'Normalize' to begin the metadata normalization process")

        self.pushButton_start = QPushButton("Normalize", self)
        self.pushButton_start.move(10, 140)
        self.pushButton_start.setEnabled(False)

        #Label with GLDS_num
        self.GLDS_num_label = QLabel(self)
        self.GLDS_num_label.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.GLDS_num_label.setGeometry(10, 170, 200, 16)

        #Label with study type
        self.study_type_label = QLabel(self)
        self.study_type_label.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.study_type_label.setGeometry(10, 195, 200, 16)

        #Label with organism
        self.organism_label = QLabel(self)
        self.organism_label.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.organism_label.setGeometry(10, 220, 200, 16)

        self.l4 = QLabel(self)
        self.l4.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.l4.setGeometry(10, 270, 200, 16)

        #Organism type icon
        self.l5 = QLabel(self)
        self.l5.setGeometry(250, 180, 100, 100)
        self.l5.hide()

        #Table
        self.table_fields = QTableWidget(self)
        self.table_fields.setGeometry(10, 290, 615, 300)
        self.table_fields.hide()

        #Label for "Investigation file was noralized"
        self.i_file_norm_label = QLabel(self)
        self.i_file_norm_label.setStyleSheet('QLabel {color:#333333; font-family:Arial; font-weight:bold; font-size:14} ')
        self.i_file_norm_label.setGeometry(10, 240, 250, 20)

        #Label for "Sample file was normalized"
        self.s_file_norm_label = QLabel(self)
        self.s_file_norm_label.setGeometry(10, 620, 360, 20)

        #Exit button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet('QPushButton {color: #004080; font-family:Arial}')
        self.exit_button.setGeometry(10, 650, 100, 20)

        #Reset button
        self.reset_button = QPushButton("Select Another File", self)
        self.reset_button.setStyleSheet('QPushButton {color: #004080; font-family:Arial}')
        self.reset_button.setGeometry(150, 650, 200, 20)
        self.reset_button.setEnabled(False)
        self.reset_button.hide()

        self.button_fields = QPushButton("Normalize Sample File", self)
        self.button_fields.setGeometry(10, 600, 200, 20)
        self.button_fields.hide()
        self.button_fields.clicked.connect(self.on_pushButton_add_fields_clicked)

        #Browse metadata file functionality
        self.pushButton_input.clicked.connect(self.on_pushButton_input_clicked)

        #Select directory functionality
        self.pushButton_output.clicked.connect(self.on_pushButton_output_clicked)
        self.dialog = FileDialog(self)

        #Normalize button functionality
        self.pushButton_start.clicked.connect(self.on_pushButton_start_clicked)

        #Add selected fields button functionality
        #self.add_fields_button3.clicked.connect(self.on_pushButton_add_fields_clicked)

        #Reset button functionality
        self.reset_button.clicked.connect(self.on_pushButton_reset_clicked)

        #Exit button functionality
        self.exit_button.clicked.connect(self.on_pushButton_exit_clicked)

        #self.add_fields_pbutton.clicked.connect(self.on_pushButton_add_fields_clicked)


    def on_pushButton_input_clicked(self):
        self.dialog.openInputFileNameDialog(self)
        if str(self.inputFile.toPlainText()) != "" and str(self.outputDir.toPlainText()) != "":
            self.pushButton_start.setEnabled(True)
            self.pushButton_start.setStyleSheet('QPushButton {color: #004080; font-family:Arial}')

    def on_pushButton_output_clicked(self):
        self.dialog.openOuputDirDialog(self)
        if str(self.inputFile.toPlainText()) != "" and str(self.outputDir.toPlainText()) != "":
            self.pushButton_start.setEnabled(True)
            self.pushButton_start.setStyleSheet('QPushButton {color: #004080; font-family:Arial}')

    def on_pushButton_start_clicked(self):
        self.pushButton_start.setEnabled(False)
        normalize(self)

    def handleItemClicked(self, item):
        row = item.row()
        if item.checkState() == QtCore.Qt.Checked:
            field_item = self.table_fields.item(row, 0)
            field = field_item.text()

            text, ok = QInputDialog.getText(self, 'Add new field', 'Enter Value for '+field+':')
            if ok:
                item.setText(str(text))
            if "age" in field or "Duration" in field or "Temperature" in field or "Growth time" in field:
                text, ok = QInputDialog.getText(self, 'Units', 'Enter Units for '+field+':')
                if ok:
                    self.table_fields.setItem(row, 3, QTableWidgetItem(text))
        else:
            #print('"%s" Clicked' % item.text())
            item.setText(str("Add Field"))
            item.setSelected(False)
            self.table_fields.setItem(row, 3, QTableWidgetItem(""))

    def on_pushButton_add_fields_clicked(self):
        self.button_fields.setEnabled(False)
        num_rows = self.table_fields.rowCount()
        dict_fields_added = {}

        for i in range(0, num_rows):
            item = self.table_fields.item(i, 2)
            if item:
                if item.checkState() == QtCore.Qt.Checked:
                    key_item = self.table_fields.item(i, 0)
                    key = str(key_item.text())
                    field =  str(item.text())
                    dict_fields_added[key] = field
                    if "age" in key or "Duration" in key or "Temperature" in key or "Growth time" in key:
                        unit_item = self.table_fields.item(i, 3)
                        unit = str(unit_item.text())
                        dict_fields_added[key] = [field, unit]

        self.dict_fields_added = dict_fields_added
        norm_s = add_extra_fields_gui(self.dict_suggestions, self.study_file, self.file_name_s, self.fields_not_found, self.flag_factor_name,self.dict_factor_name, self.dict_sf_modified, self.no_suggestions, self.dict_fields_added)
        outdir = self.outdir
        f4 = open(os.path.join(outdir, self.file_name_s), "w+")
        f4.write(norm_s)
        f4.close()

        self.s_file_norm_label.setText("Sample file was normalized and selected fields were added...")

    def on_pushButton_reset_clicked(self):
        self.inputFile.setText("")
        self.outputDir.setText("")
        self.GLDS_num_label.setText("")
        self.organism_label.setText("")
        self.study_type_label.setText("")
        self.table_fields.hide()
        self.reset_button.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.i_file_norm_label.setText("")
        self.s_file_norm_label.setText("")
        self.l4.hide()
        self.l5.hide()


    def on_pushButton_exit_clicked(self):
        sys.exit()

def fill_table(fields_not_found, fields_found, main_w):
    main_w.button_fields.show()
    main_w.table_fields.setColumnCount(4)
    header = main_w.table_fields.horizontalHeader()
    main_w.table_fields.setHorizontalHeaderLabels(["Field","Found/Not Found", "Add field", "Units"])
    header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    num_fields_found = 0
    num_fields_not_found = 0
    for letter in fields_found:
        if letter == "\n":
            num_fields_found +=1
    for letter in fields_not_found:
        if letter == "\n":
            num_fields_not_found +=1
    main_w.table_fields.setRowCount(num_fields_found+num_fields_not_found)

    field = ""
    i=0
    for letter in fields_found:
        field = field+letter
        if letter == "\n":
            field = field[:-1]
            main_w.table_fields.setItem(i, 0, QTableWidgetItem(field))
            main_w.table_fields.setItem(i, 1, QTableWidgetItem("FOUND"))
            field= ""
            i+=1

    field = ""
    for letter in fields_not_found:
        field = field + letter
        if letter == "\n":
            field = field[:-1]
            main_w.table_fields.setItem(i, 0, QTableWidgetItem(field))
            main_w.table_fields.setItem(i, 1, QTableWidgetItem("NOT FOUND"))
            field = ""
            i+=1

    i=0
    for i in range(num_fields_found, num_fields_found+num_fields_not_found):
        item = QTableWidgetItem('Add Field')
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        main_w.table_fields.setItem(i, 2, item)


    main_w.table_fields.itemClicked.connect(main_w.handleItemClicked)


    main_w.table_fields.show()


def normalize(main_w):
    metadata_directory = main_w.metadata_directory
    outdir = main_w.outdir

    dirpath = metadata_directory
    #entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    #entries = ((os.stat(path), path) for path in entries)
    #entries = ((stat[ST_MTIME], path) for stat, path in entries)
    GLDS = os.path.basename(os.path.dirname(metadata_directory))
    metadata_out = GLDS
    i = 0

    GLDS_num = ""
    path = str(main_w.inputFile.toPlainText())
    name = os.path.basename(path)
    if 'zip' in path and i == 0:
        flag = 0
        #path2 = path[::-1]
        for letter in path:
            if flag ==1:
                #print(letter)
                GLDS_num = GLDS_num + letter
            if letter == "-" or letter == "_":
                flag+=1

        #metadata_zip = os.path.join(metadata_directory,os.path.basename(path))
            #cp_command = ["cp","-r",metadata_zip,metadata_out]

        cp_command = ["cp","-r",metadata_directory,os.path.basename(os.path.dirname(outdir))]
        unzip_command = ["unzip", "-o", "-qq",metadata_directory,"-d", outdir]

        remove_zip_command = ["rm",os.path.join(outdir, name)]
        subprocess.call(cp_command)
        subprocess.call(unzip_command)
        #else:
            #cp_command = ["cp","-r",metadata_directory,os.path.basename(os.path.dirname(outdir))]
            #subprocess.call(cp_command)

    dirs_array = ""
    for root, dirs, files in os.walk(outdir):
        for directory in dirs:
            dirs_array = dirs_array + directory + "."
            #directory = ""

    directory = ""

    GLDS_num = str(GLDS_num[:-1])

    #Try creating label before and just updating text
    main_w.GLDS_num_label.setText("GLDS-"+GLDS_num)

    [study_type, organism]=find_study_type(int(GLDS_num))
    organism_img = get_organism_image(organism)

    pixmap = QPixmap(organism_img)
    main_w.l5.setPixmap(pixmap)

    main_w.study_type_label.setText("STUDY TYPE: "+study_type)
    main_w.organism_label.setText("ORGANISM: "+organism)
    main_w.l5.show()
    #print("Organism type: ", study_type)

    #Type of study
    #study_type = input("Chose study type:\n 1.Non-mammals \n 2.Cell lines \n 3.Microbes \n 4.Mammals \n 5.Plants \n")
    if study_type == "Non-mammal":
        required_fields_file = "required_fields_nonmammals.txt"
        keywords_file = "keywords_nonmammals.txt"
    elif study_type=="Cell line":
        required_fields_file = "required_fields_celllines.txt"
        keywords_file = "keywords_celllines.txt"
    elif study_type=="Microbe":
        required_fields_file = "required_fields_microbes.txt"
        keywords_file = "keywords_microbes.txt"
    elif study_type=="Mammal":
        required_fields_file = "required_fields_mammals.txt"
        keywords_file = "keywords_mammals.txt"
    elif study_type=="Plant":
        required_fields_file = "required_fields_plants.txt"
        keywords_file = "keywords_plants.txt"

    [study_file, investigation_file, file_name_s, file_name_i] = get_files(metadata_directory, outdir)

    #Investigation file normalization
    print("Normalizing investigation file...")
    [normalized_inv, flag_factor_name, dict_factor_name, dict_sf_modified, dict_dates_modified]  = normalize_inv_file(investigation_file)

    main_w.i_file_norm_label.setText("Investigation file was normalized...")
    main_w.reset_button.show()
    main_w.l4.setText("Sample File fields:")
    main_w.reset_button.setEnabled(True)

    try:
        #f5 = open(os.path.join(metadata_directory, file_name_i), "w")
        f5 = open(os.path.join(outdir, file_name_i), "w+")
        f5.write(normalized_inv)
        f5.close()
    except Exception as e:
        print(e, "\n Error overwriting investigation file.")

    #Sample file normalization
    print("Normalizing sample file...")
    [fields_not_found, fields_found] = check_required_fields(required_fields_file, study_file)

    #main_w.fields_found_label.setText("Fields found:\n"+fields_found)
    #main_w.fields_notfound_label.setText("Fields not found:\n"+fields_not_found)
    #main_w.rbutton1.show()

    fill_table(fields_not_found, fields_found, main_w)
    #main_w.add_fields_pbutton.show()
    #main_w.add_fields_button.setEnabled(True)
    #main_w.add_fields_button.setStyleSheet('QPushButton {color: #004080; font-family:Arial; background-color:white}')

    # add_files_flag = input("\nWould you like to add the missing fields? (y/n):")
    # if add_files_flag == "y":
    dict_suggestions = {}
    #     dict_suggestions = find_seuggestions(keywords_file, fields_not_found)
    no_suggestions =""

    main_w.dict_suggestions = dict_suggestions
    main_w.study_file = study_file
    main_w.file_name_s = file_name_s
    main_w.fields_not_found = fields_not_found
    main_w.flag_factor_name = flag_factor_name
    main_w.dict_factor_name = dict_factor_name
    main_w.dict_sf_modified = dict_sf_modified
    main_w.no_suggestions = no_suggestions

    #     generate_report(metadata_directory, str(GLDS_num), file_name_i, dict_dates_modified, dict_sf_modified, dict_field_added, file_name_s, dict_factor_name)
    #     input("Investigation and Sample files were normalized.\nPress enter to continue")
    # elif add_files_flag == "n":
    #     print("Investigation file was normalized.\n No new fields were added to the Sample File.")
    #     #Change facrtor name in study file
    #     if flag_factor_name == 1:
    #         line_num=0
    #         header = ""
    #         for letter in study_file:
    #             if line_num==0:
    #                 header = header + letter
    #             if letter == "\n":
    #                 line_num += 1
    #         temp = header
    #         for key, values in dict_sf_modified.items():
    #             header2 = temp.replace(values[0], values[1])
    #             temp = header2
    #         dict_field_added={}
    #
    #         study_file = study_file.replace(header, header2)
    #         #f4 = open(os.path.join(metadata_directory, file_name_s), "w")
    #         f4 = open(os.path.join(outdir, file_name_s), "w+")
    #         f4.write(study_file)
    #         f4.close()
    #     else:
    #         dict_field_added = {}
    #
    #     generate_report(metadata_directory, str(GLDS_num), file_name_i, dict_dates_modified, dict_sf_modified, dict_field_added, file_name_s, dict_factor_name)
    #     input("Press enter to continue")
    #     #sys.exit()
    # elif add_files_flag == "exit":
    #     sys.exit()
    # else:
    #     print("Please enter a valid option or 'exit' to leave...")


def main():
    app = QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
