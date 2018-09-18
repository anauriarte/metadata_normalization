from normalize_metadata import norm
import os
from stat import ST_MTIME
import os, sys, time, subprocess

from PyQt5 import QtGui, QtWidgets

def window():
   app = QtWidgets.QApplication(sys.argv)
   w = QtWidgets.QWidget()
   b = QtWidgets.QLabel(w)
   b.setText("Hello World!")
   w.setGeometry(100,100,200,50)
   b.move(50,20)
   #w.setWindowTitle(“PyQt”)
   w.show()
   sys.exit(app.exec_())

def clean(metadata_directory,outdir):
    #Path to the directory (absolute)
    dirpath = metadata_directory

    #Get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)

    #Insert creation date so we can get the last modified metadata
    entries = ((stat[ST_MTIME], path) for stat, path in entries)

    #Find name of GLDS number
    #GLDS = ISACreator-1.7.10GeneLab 2
    GLDS = os.path.basename(os.path.dirname(outdir))
    metadata_out = GLDS

    #Make appropriate output directory
    if not os.path.exists(metadata_out):
        os.makedirs(metadata_out)

    #Get last modified metadata zip file, copy to the output directory, unzip it, remove the zipped directory, and finally bring all files within folders to the top metadata directory
    i = 0
    for cdate, path in sorted(entries,reverse=True):
        name = os.path.basename(path)
        if 'zip' in path and i == 0:
            metadata_zip = os.path.join(metadata_directory,os.path.basename(path))

            #Copy the last modified metadata
            cp_command = ["cp","-r",metadata_zip,metadata_out]
            #print (' '.join(cp_command))
            #Unzip it into the metadata_out directory
            #unzip_command = ["unzip", "-o", "-qq",os.path.join(metadata_out,os.path.basename(metadata_zip)),"-d",metadata_out]
            unzip_command = ["unzip", "-o", "-qq",os.path.join(metadata_directory, name),"-d", outdir]
            #Remove the .zip compressed file to avoid confusion and save space
            #remove_zip_command = ["rm",os.path.join(metadata_out,os.path.basename(metadata_zip))]
            remove_zip_command = ["rm",os.path.join(outdir, name)]

            #Execute commands
            subprocess.call(cp_command)
            subprocess.call(unzip_command)
            #subprocess.call(remove_zip_command)
            i += 1

    for files in os.walk(outdir):
        for filename in files:
            name = filename
    flag = 0
    GLDS_num = ""
    for string in name:
        filename = string
    for letter in filename:
        if letter == "-" or letter == "_":
            flag += 1
        if flag ==2:
            GLDS_num = GLDS_num + letter
    GLDS_num = GLDS_num[1:]

    return int(GLDS_num)

while True:
    try:
        #Metadata folder directory
        #window()
        os.system('clear')
        print("METADATA NORMALIZATION \n Enter 'exit' to leave...")
        metadata_directory = input("Name of the metadata directory: ")
        if metadata_directory == "exit":
            break;
        outdir = input("Name of the output directory:")
        if outdir == "exit":
            break;
        #GLDS_num = clean(metadata_directory, outdir)
    except Exception as e:
        print(e, "\nPress enter to try another directory...")
        input()
    else:
        dirpath = metadata_directory
        entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
        entries = ((os.stat(path), path) for path in entries)
        entries = ((stat[ST_MTIME], path) for stat, path in entries)
        GLDS = os.path.basename(os.path.dirname(metadata_directory))
        metadata_out = GLDS
        i = 0
        GLDS_num_array=""
        for cdate, path in sorted(entries,reverse=True):
            name = os.path.basename(path)


            if 'zip' in path and i == 0:
                flag = 0
                path2 = path[::-1]
                #print(path2)
                for letter in path2:
                    if flag ==4:
                        #print(letter)
                        GLDS_num_array = GLDS_num_array + letter
                    if flag==5:
                        GLDS_num_array = GLDS_num_array + "."
                        flag+=1
                    if letter == "-" or letter == "_":
                        flag+=1

                metadata_zip = os.path.join(metadata_directory,os.path.basename(path))
                #cp_command = ["cp","-r",metadata_zip,metadata_out]
                cp_command = ["cp","-r",metadata_zip,os.path.basename(os.path.dirname(outdir))]
                unzip_command = ["unzip", "-o", "-qq",os.path.join(metadata_directory, name),"-d", outdir]
                remove_zip_command = ["rm",os.path.join(outdir, name)]
                subprocess.call(cp_command)
                subprocess.call(unzip_command)
            #else:
                #cp_command = ["cp","-r",metadata_directory,os.path.basename(os.path.dirname(outdir))]
                #subprocess.call(cp_command)
        GLDS_num_array = "." + GLDS_num_array
        dirs_array = ""
        for root, dirs, files in os.walk(outdir):
            for directory in dirs:
                dirs_array = dirs_array + directory + "."
                #directory = ""

        #print(dirs_array)
        i=0
        GLDS_num_array = GLDS_num_array[::-1]
        GLDS_num_array = GLDS_num_array[1:]
        #print(GLDS_num_array)
        #print(dirs_array)

        directory = ""
        for letter in dirs_array:
            directory = directory + letter
            if letter == ".":
                GLDS_num = ""
                temp=""
                j= 0
                for letter2 in GLDS_num_array:
                    #if letter2.isdigit():
                    temp = temp + letter2
                    if letter2 == ".":
                        if j==i:
                            #print("entra")
                            GLDS_num = temp[:-1]
                        else:
                            temp = ""
                        j+=1
                GLDS_num=GLDS_num[1:]
                #print(GLDS_num)
                directory = directory[:-1]
                #print(directory)
                full_dir = os.path.join(outdir, directory)

                #print(GLDS_num)
                #print(full_dir)
                norm(metadata_directory, full_dir, int(GLDS_num))

                directory = ""
                i+= 1
