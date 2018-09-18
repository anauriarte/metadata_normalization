
import fileinput
import re
from stat import ST_MTIME
#import PyPDF2
import os, sys, time, subprocess
import csv

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
    GLDS = os.path.basename(os.path.dirname(metadata_directory))
    #metadata_out is the path to the output metadata
    #metadata_out = os.path.join(outdir,GLDS,'metadata')
    #metadata_out = os.path.join(outdir,GLDS)
    metadata_out = GLDS

    #Make appropriate output directory
    #if not os.path.exists(metadata_out):
    #    os.makedirs(metadata_out)

    #Get last modified metadata zip file, copy to the output directory, unzip it, remove the zipped directory, and finally bring all files within folders to the top metadata directory
    i = 0
    for cdate, path in sorted(entries,reverse=True):
        name = os.path.basename(path)
        if 'zip' in path and i == 0:
            #Get GLDS number


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

    #Loop through the metadata_out directory in case the unzipping produces a folder. If so, mv contents of folder up one directory and remove folder
    #for filename in os.listdir(metadata_out):
        #if os.path.isdir(os.path.join(metadata_out,filename)):
            #move_command = ["mv", os.path.join(metadata_out,filename,"*"),metadata_out]
            #remove_folder_command = ["rm", "-r",os.path.join(metadata_out,filename)]
            #subprocess.call(move_command)
            #subprocess.call(remove_folder_command)
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

def get_organism_image(organism):
    if organism=="Mus musculus" or organism=="Rattus norvegicus":
            image_name = "rodent.jpeg"
    elif organism == "Homo sapiens":
            image_name = "human.jpeg"
    elif organism=="Arabidopsis thaliana" or organism=="Brassica rapa" or organism=="Ceratopteris richardii":
            image_name = "plant.jpeg"
    elif (organism == "Aspergillus fumigatus" or organism=="Bacillus"or organism=="Bacillus subtilis" or organism=="Candida albicans" or\
          organism == "Escherichia coli" or organism=="vibrio" or organism=="Klebsiella" or organism=="Staphylococcus" or organism=="Pantoea conspicus" or\
          organism=="Enterobacter" or organism=="Microbiota" or organism=="Mycobacterium marinum" or organism=="Pseudomonas aeruginosa" or\
          organism == "Rhodospirilium rubrum" or organism=="Saccharomyces cerevisiae" or organism == "Salmonella enterica" or\
          organism == "Staphylococcus aureus" or organism=="Streptococcus mutans" or organism=="Trichoderma virens" or organism == "Aspergillus terreus" or\
          organism == "Aurebasidium pullulans"):
            image_name = "microbe.jpeg"
    elif organism == "Caenorhabditis elegans":
            image_name = "worm.jpeg"
    elif organims == "Danio rerio" or organism == "Daphnia magna" or organism=="Euprymna scolopes" or organism == "Oryzias latipes":
            image_name = "fish.jpeg"
    elif organism=="Drosophila melanogaster":
            image_name = "fly.jpeg"

    return image_name
def find_study_type(GLDS_num):
    study_type = ""
    print("GLDS-", GLDS_num)
    try:
        file = open('All-Table 1.txt', 'r')
        text = file.read();
        row = ""
        i=0
        GLDS_info = ""
        for letter in text:
            row = row + letter
            if letter == "\n":
                if GLDS_num > 1:
                    if i == GLDS_num+1:
                        print(i)
                        GLDS_info = row
                elif GLDS_num == 1:
                    if i == GLDS_num:
                        GLDS_info = row
                row = ""
                i+=1

        flag = 0
        organism = ""
        for letter in GLDS_info:
            if letter == ",":
                flag +=1
            if flag == 1:
                organism = organism + letter
        organism=organism[1:]

        print("Organism: ", organism)

        if organism=="Mus musculus" or organism=="Homo sapiens" or organism=="Rattus norvegicus":
            study_type = "Mammal"
        elif organism=="Arabidopsis thaliana" or organism=="Brassica rapa" or organism=="Ceratopteris richardii":
            study_type = "Plant"
        elif (organism == "Aspergillus fumigatus" or organism=="Bacillus"or organism=="Bacillus subtilis" or organism=="Candida albicans" or\
            organism == "Escherichia coli" or organism=="vibrio" or organism=="Klebsiella" or organism=="Staphylococcus" or organism=="Pantoea conspicus" or\
            organism=="Enterobacter" or organism=="Microbiota" or organism=="Mycobacterium marinum" or organism=="Pseudomonas aeruginosa" or\
            organism == "Rhodospirilium rubrum" or organism=="Saccharomyces cerevisiae" or organism == "Salmonella enterica" or\
            organism == "Staphylococcus aureus" or organism=="Streptococcus mutans" or organism=="Trichoderma virens" or organism == "Aspergillus terreus" or\
            organism == "Aurebasidium pullulans"):
            study_type = "Microbe"
        elif (organism == "Caenorhabditis elegans" or organism=="Danio rerio" or organism =="Daphnia magna" or organism=="Drosophila melanogaster" or\
            organism=="Euprymna scolopes" or organism == "Oryzias latipes"):
            study_type = "Non-mammal"
        elif organism == "environmental samples" or organism == "Home":
            print("No known organism type")
        else:
            print("ERROR: No known organism type")
            sys.exit()

    except Exception as e:
        print(e, "\n Error opening GLDS table, please make sure the file 'All-Table 1.csv' is in the right directory and try again. ")
        sys.exit()

    return study_type, organism

def get_files(metadata_directory, outdir):
    file_name_s = ""
    file_name_i  = ""
    study_file = ""
    investigation_file = ""
    dir = ""
    for root, dirs, files in os.walk(outdir):
        for element in dirs:
            dir = element
        for filename in files:
            if filename[0]=="s":
                file_name_s = outdir+"/"+dir+"/"+filename
                try:
                    f1 = open(os.path.join(metadata_directory, file_name_s), "r", encoding='windows-1252')
                    study_file = f1.read()
                    f1.close()
                except Exception as e:
                    print(e)
            if filename[0]=="i":
                file_name_i = outdir+"/"+dir+"/"+filename
                #print(os.path.join(metadata_directory, file_name_i))
                try:
                    f2 = open(os.path.join(metadata_directory, file_name_i), "r", encoding='windows-1252')
                    investigation_file = f2.read()
                    f2.close()
                except Exception as e:
                    print(e)
    if file_name_s == "":
        print("ERROR: No sample file found. Please make sure the metadata files are complete and named correctly.")
        sys.exit()
    else:
        if study_file == "":
            print("ERROR: The study file is empty.")
            sys.exit()
    if file_name_i == "":
        print("ERROR: No investigation file found. Please make sure the metadata files are complete and named correctly.")
        sys.exit()
    else:
        if investigation_file == "":
            print("Error: The investigation file is empty.")
            sys.exit()
    return [study_file, investigation_file, file_name_s, file_name_i]

def change_dateformat(invesitgation_file):

    line = ""
    correct_file = ""
    dict_dates_modified = {}
    for letter in invesitgation_file:
        line = line + letter
        if letter == "\n":
            if "Investigation Submission Date" in line or\
                "Investigation Public Release Date" in line or\
                "Comment[Created with configuration]" in line or\
                "Comment[Created With Configuration]" in line or\
                "Study Publication Release Date" in line or\
                "Study Submission Date" in line or\
                "Comment[Mission Start]" in line or\
                "Comment[Mission End]" in line:
                flag = 0
                date = ""
                for letter2 in line:
                    if letter2 == "\"":
                        flag+=1
                    if flag == 1:
                        date = date + letter2
                if date is not "\"":
                    date = date[1:]
                    #get day month and year
                    temp = ""
                    flag2=0
                    reset = 0
                    ambiguous_flag = 0
                    invalid_date = 0
                    first = ""
                    second = ""
                    third = ""
                    for letter3 in date:
                        temp = temp + letter3
                        if letter3 == "/" or letter3 == "-" or letter3 == "." or letter3 == "_":
                            reset = 1
                            flag2 += 1
                        if flag2 == 1 and reset == 1:
                            first = temp[:-1]
                            reset = 0
                            temp = ""
                        if flag2 == 2 and reset == 1:
                            second = temp[:-1]
                            reset = 0
                            temp = ""
                    third = temp

                    #check length of strings to try to figure out format
                    if (len(first) == 2 and len(second) == 2 and len(third) == 2) or (len(first) == 2 and len(second) == 2 and len(third) == 4):
                        #Assume last term is year
                        year = third
                        #Check if one of the terms is bigger than 12
                        if int(first) > 12:
                            day = first
                            month = second
                        elif int(second) > 12:
                            day = second
                            month = first
                        else:
                            ambiguous_flag = 1
                    elif (len(first) == 1 and len(second) == 2 and len(third) == 2) or (len(first) == 1 and len(second) == 2 and len(third) == 4):
                        #Assume last term is year
                        year = third
                        #Check if one of the terms is bigger than 12
                        if int(first) > 12:
                            day = first
                            month = second
                        elif int(second) > 12:
                            day = second
                            month = first
                        else:
                            ambiguous_flag = 1
                    elif (len(first) == 2 and len(second) == 1 and len(third) == 2) or (len(first) == 2 and len(second) == 1 and len(third) == 4):
                        #Assume last term is year
                        year = third
                        #Check if one of the terms is bigger than 12
                        if int(first) > 12:
                            day = first
                            month = second
                        elif int(second) > 12:
                            day = second
                            month = first
                        else:
                            ambiguous_flag = 1
                    elif (len(first) == 2 and len(second) == 3 and len(third) == 2) or (len(first) == 2 and len(second) == 3 and len(third) == 4):
                        year = third
                        month = second
                        day = first
                    elif (len(first) == 1 and len(second) == 3 and len(third) == 2) or (len(first) == 1 and len(second) == 3 and len(third) == 4):
                        year = third
                        month = second
                        day = first
                    elif (len(first) == 3 and len(second) == 2 and len(third) == 2) or (len(first) == 3 and len(second) == 2 and len(third) == 4):
                        year = third
                        month = first
                        day = second
                    else:
                        if date != "\"":
                            print(date)
                            ambiguous_flag = 1

                    if ambiguous_flag == 0:
                        #Change month format to MMM
                        if len(month) != 3:
                            if int(month) == 1:
                                month = "Jan"
                            elif int(month) == 2:
                                month = "Feb"
                            elif int(month) == 3:
                                month = "Mar"
                            elif int(month) == 4:
                                month = "Apr"
                            elif int(month) == 5:
                                month = "May"
                            elif int(month) == 6:
                                month = "Jun"
                            elif int(month) == 7:
                                month = "Jul"
                            elif int(month) == 8:
                                month = "Aug"
                            elif int(month) == 9:
                                month = "Sep"
                            elif int(month) == 10:
                                month = "Oct"
                            elif int(month) == 11:
                                month = "Nov"
                            elif int(month) == 12:
                                month = "Dec"
                            else:
                                print("ERROR: Invalid date. Month must be bigger than 0 and smaller than 12")
                                invalid_date = 1
                        #Change year to YYYY
                        if year.isdigit():
                            if len(year) != 4:
                                if int(year)<50:
                                    year = "20" + year
                                else:
                                    year = "19" + year

                        #Check that day is smaller than 31
                        if day.isdigit():
                            if int(day) >31 or int(day) < 0:
                                print("ERROR: Invalid date. Day must be smaller than 31 and bigger than 0.")
                                invalid_date = 1

                        new_date = day + "-" + month + "-" + year

                        if invalid_date == 0:
                            line = line.replace(date, new_date)
                            dict_dates_modified[line] = [date, new_date]
                        else:

                            input("Cannot change date format.\n Unknown date format or can't tell month and day.")
                    else:
                        input("Cannot change date format.\n Unknown date format or can't tell month and day.")

            correct_file = correct_file + line
            line = ""
    return correct_file, dict_dates_modified

def normalize_inv_file(investigation_file):
    #Dictionary of current factor name and new values:
    currentfactor_spacefligth = ["microgravity","gravitation","space flight","gravity","treatment","weightlessness","extraterrestrial environment","environmental stress", "Spaceflight"]
    currentfactor_time = ["timepoint", "sampling time", "time", "Time"]
    currentfactor_radiation = ["Radiation", "Radiation Ionizing", "irradiation", "response to ionizing radiation", "radiation", "irradiate", "radiation type"]
    currentfactor_treatmentdose = ["treatment dose"]
    currentfactor_radiationdose = ["radiation dose", "absorbed radiation dose"]
    currentfactor_condition = ["condition"]
    currentfactor_treatment = ["treatment protocol", "plant treatment", "clinical treatment", "clinical treatment", "bleomycin treatment"]

    dict_newvals ={}
    dict_newvals["Spaceflight"]=["Spaceflight", "Space Flight", "http://bioportal.bioontology.org/ontologies/MESH?p=classes&conceptid=http://purl.bioontology.org/ontology/MESH/D013026", "MESH"]

    dict_newvals["treatment protocol"] = ["treatment protocol", "treatment", "http://www.ebi.ac.uk/efo/EFO_0000727", "EFO"]
    dict_newvals["plant treatment"] = ["plant treatment", "treatment", "http://www.ebi.ac.uk/efo/EFO_0000727", "EFO"]
    dict_newvals["clinical treatment"] = ["clinical treatment", "treatment", "http://www.ebi.ac.uk/efo/EFO_0000727", "EFO"]
    dict_newvals["bleomycin treatment"] = ["bleomycin treatment", "treatment", "http://www.ebi.ac.uk/efo/EFO_0000727", "EFO"]

    dict_newvals["Time"] = ["Time", "Time", "http://www.ebi.ac.uk/efo/EFO_0000721", "EFO"]

    dict_newvals["Radiation"] = ["Ionizing Radiation", "Ionizing Radiation", "https://evs.nci.nih.gov/ftp1/rdf/Thesaurus.owl#C17052", "NCIT"]

    dict_newvals["treatment dose"] = ["dose", "dose", "http://purl.obolibrary.org/obo/OBI_0000984", "OBI"]

    dict_newvals["radiation dose"] = ["Absorbed radiation dose", "Absorbed Radiation Dose", "https://evs.nci.nih.gov/ftp1/rdf/Thesaurus.owl#C95181", "NCIT"]

    dict_newvals["condition"] = ["Microgravity simulation", "Weightlessness simulation", "http://bioportal.bioontology.org/ontologies/MESH?p=classes&conceptid=D018474", "MESH "]

    dict_newvals[""] = []
    #Change date formats
    [investigation_file, dict_dates_modified] = change_dateformat(investigation_file)

    #Get lines
    line = ""
    normalized_file=""
    factor_name = ""
    accession_num = ""
    source_ref = ""
    factor_type = ""
    flag_factor_name = 0
    dict_factor_name = {}
    dict_sf_modified = {}
    for letter in investigation_file:
        line = line + letter
        if letter == "\n":
            #Replace study factor name
            if "Study Factor Name" in line:
                flag=0
                factor_name =""
                factor_name_array = ""
                key_dict_array  = ""
                flag2 = 0
                for letter2 in line:
                    if letter2=="\"":
                        flag+=1
                    if flag % 2 == 1:
                        factor_name = factor_name + letter2
                    elif flag%2 == 0 and flag > 0 and letter2 is not "	" and letter2 is not "\n":
                        factor_name = factor_name[1:]
                        key_dict= ""

                        flag2=0
                        num_matches = 0
                        factor_name_array = factor_name_array  + factor_name + "."
                        for word in currentfactor_spacefligth:
                            str =  "\\b{}\\b".format(word)
                            match = re.search(str, factor_name, re.IGNORECASE)
                            if match:
                                print(factor_name)
                                num_matches += 1
                                flag2+=1
                                key_dict = "Spaceflight"
                        for word in currentfactor_time:
                            str =  "\\b{}\\b".format(word)
                            match = re.search(str, factor_name, re.IGNORECASE)
                            if match:
                                num_matches += 1
                                flag2+=1
                                key_dict = "Time"
                        for word in currentfactor_condition:
                            str =  "\\b{}\\b".format(word)
                            match = re.search(str, factor_name, re.IGNORECASE)
                            if match:
                                num_matches += 1
                                flag2+=1
                                key_dict = "condition"
                        for word in currentfactor_radiation:
                            str =  "\\b{}\\b".format(word)
                            match = re.search(str, factor_name, re.IGNORECASE)
                            if match:
                                num_matches += 1
                                flag2+=1
                                str =  "\\b{}\\b".format("dos")
                                match2 = re.search(str, factor_name, re.IGNORECASE)
                                if "dos" in factor_name:
                                    flag2+=1
                                    key_dict = "radiation dose"
                                else:
                                    key_dict = "Radiation"
                        for word in currentfactor_treatment:
                             str =  "\\b{}\\b".format(word)
                             match = re.search(str, factor_name, re.IGNORECASE)
                             if match:
                                 num_matches += 1
                                 flag2+=1
                                 #key_dict = word
                                 str =  "\\b{}\\b".format("dos")
                                 match2 = re.search(str, factor_name, re.IGNORECASE)
                                 if "dos" in factor_name:
                                     flag2+=1
                                     key_dict = "treatment dose"
                                 else:
                                     key_dict = word
                        if flag2>0:

                            key_dict_array = key_dict_array + key_dict + "."
                        factor_name = ""

                #Check if there is more than one factor name
                num_factornames = flag/2

                #Check study factor
                iterations = 0
                while iterations < num_factornames:
                    cont = 0
                    temp = ""
                    for letter3 in factor_name_array:
                        temp= temp + letter3
                        if letter3 == ".":
                            temp = temp[:-1]
                            cont += 1
                            if cont == iterations + 1:
                                factor_name = temp
                            else:
                                temp = ""
                    cont = 0
                    temp = ""


                    for letter3 in key_dict_array:
                        temp= temp + letter3
                        if letter3 == ".":
                            temp = temp[:-1]
                            cont += 1
                            if cont == iterations + 1:
                                key_dict = temp
                            else:
                                temp = ""

                    if flag2>0:
                        line = line.replace(factor_name, dict_newvals[key_dict][0])
                        name = "Study Factor Name     " + factor_name
                        dict_sf_modified[name] = [factor_name, dict_newvals[key_dict][0]]
                        flag_factor_name = 1
                        dict_factor_name[key_dict] = dict_newvals[key_dict][0]
                    else:
                        print("No new Factor Name for: ", factor_name)
                    iterations += 1
                normalized_file = normalized_file + line

            #Replace study factor type
            elif "Study Factor Type" in line:
                iterations = 0
                while iterations < num_factornames:
                    cont = 0
                    temp = ""
                    for letter3 in factor_name_array:
                        temp= temp + letter3
                        if letter3 == ".":
                            temp = temp[:-1]
                            cont += 1
                            if cont == iterations +1:
                                factor_name = temp
                            else:
                                temp = ""
                    cont = 0
                    temp = ""
                    for letter3 in key_dict_array:
                        temp= temp + letter3
                        if letter3 == ".":
                            temp = temp[:-1]
                            cont += 1
                            if cont == iterations +1:
                                key_dict = temp
                            else:
                                temp = ""

                    if "Term Accession Number" in line:
                        flag=0
                        accession_num =""
                        for letter2 in line:
                            if letter2=="\"":
                                flag+=1
                            if flag == iterations + iterations + 1:
                                accession_num = accession_num + letter2
                        accession_num = accession_num[1:]

                        if flag2>0:
                            line = line.replace(accession_num, dict_newvals[key_dict][2])
                            name = "Study Factor Type Term Accession Number     " + accession_num
                            dict_sf_modified[name] = [accession_num, dict_newvals[key_dict][2]]
                        else:
                            print("No new Study Factor Type Term Accession Number for: ", accession_num)
                        #normalized_file = normalized_file + line
                    elif "Term Source REF" in line:
                        flag=0
                        source_ref =""
                        for letter2 in line:
                            if letter2=="\"":
                                flag+=1
                            if flag == iterations + iterations + 1:
                                source_ref = source_ref + letter2
                        source_ref = source_ref[1:]
                        if flag2>0:
                            line = line.replace(source_ref, dict_newvals[key_dict][3])
                            name = "Study Factor Type Term Source REF   "+source_ref
                            dict_sf_modified[name] = [source_ref, dict_newvals[key_dict][3]]
                        else:
                            print("No new Study Factor Type Term Source REF for: ", source_ref)
                        #normalized_file = normalized_file + line
                    else:
                        flag=0
                        factor_type =""

                        for letter2 in line:
                            if letter2=="\"":
                                flag+=1
                            if flag == iterations + iterations + 1:
                                factor_type = factor_type + letter2
                        factor_type = factor_type[1:]
                        if flag2>0:
                            line = line.replace(factor_type, dict_newvals[key_dict][1])
                            name  = "Study Factor Type      "+factor_type
                            dict_sf_modified[name] = [factor_type, dict_newvals[key_dict][1]]
                        else:
                            print("No new Study Factor Type for: ", factor_type)
                        #normalized_file = normalized_file + line
                    iterations += 1
                normalized_file = normalized_file + line
            else:
                normalized_file = normalized_file  + line

            line = ""

    if factor_name == "":
        print("ERROR: No Study Factor Name specified in the Investigation File.\nPlease verify the investigation file and try again")
        sys.exit()
    if accession_num == "":
        print("ERROR: No Study Factor Type Term Accession Number specified in the Investigation File.\nPlease verify the investigation file and try again")
        sys.exit()
    if source_ref == "":
        print("ERROR: No Study Factor Type Term Source REF specified in the Investigation File.\nPlease verify the investigation file and try again")
        sys.exit()
    if factor_type == "":
        print("ERROR: No Study Factor Type specified in the Investigation File.\nPlease verify the investigation file and try again")
        sys.exit()

    return normalized_file, flag_factor_name, dict_factor_name, dict_sf_modified, dict_dates_modified

def check_required_fields(required_fields_file, study_file):
    fields_not_found = ""
    fields_found = ""
    first_row = ""
    try:
        required_fields = open(required_fields_file, "r")
        fields = required_fields.read()
        required_fields.close()
    except Exception as e:
        print(e, "\n ERROR: file with required fields not found. \n Please make sure the file ", required_fields_file, " is in the right directory and try again.")
        sys.exit()
    else:
        #Get header from study file
        line_num=0
        header = ""
        for letter in study_file:
            if line_num==0:
                header = header + letter
            if line_num ==1:
                first_row = first_row + letter
            if letter == "\n":
                line_num += 1
        #Check if header contains required fields
        word=""
        for letter in fields:
            word = word + letter
            if letter == "\n":
                flag =0
                field = ""
                word = word[:-1]
                for letter2 in word:
                    if letter2 == "[" or letter2=="]":
                        flag+=1
                    if flag == 1:
                        field = field + letter2
                field = field[1:]
                if flag == 0:
                    field = word

                #str =  "\\b{}\\b".format(word)
                str =  "\\b{}\\b".format(field)
                match = re.search(str, header, re.IGNORECASE)
                if match:
                    print(word, "FOUND")
                    fields_found = fields_found + word + "\n"
                else:
                    fields_not_found = fields_not_found + word + "\n"
                word = ""
                field = ""

        print("\n\nThe following fields were not found:")
        for letter in fields_not_found:
            print(letter, end="")


        return fields_not_found, fields_found

def find_seuggestions(keywords_file, fields_not_found):
    dict_suggestions= {}
    extra_info=""
    while True:
        try:
            extra_file_name = input("File with extra info (press enter to continue without a file):")

            #if the file is a PDF
            if extra_file_name[-3:] == "pdf":
                pdfFileObj = open(extra_file_name,'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
                num_pages = pdfReader.numPages
                count = 0
                extra_info = ""
                while count < num_pages:
                    pageObj = pdfReader.getPage(count)
                    extra_info += pageObj.extractText()
                    count +=1
                break;
            elif extra_file_name[-3:] == "txt":
                f3 = open(extra_file_name, "r")
                extra_info = f3.read()
                f3.close()
                break;
            elif extra_file_name == "":
                break;
            else:
                print("Please enter a valid file (.pdf or .txt)...")
        except Exception as e:
            print(e)

    sentence = ""
    if extra_info is not "":
        for letter in extra_info:
            sentence = sentence + letter
            if letter == ".":
                #Check if sentece containd keywords for fields
                try:
                    f4 = open(keywords_file, "r")
                    keywords = f4.read()
                    f4.close()
                except Exception as e:
                    print(e, "\nERROR: File containing keywords for study type not found.\nPlease make sure the file ", keywords_file, " is in the right directory and try again.")
                else:
                    field = ""
                    string_add_column = ""
                    keyword = ""
                    string_field = ""
                    matching_sentences=""
                    no_suggestions = ""
                    for letter in keywords:
                        field = field + letter
                        keyword = keyword + letter
                        #End of a line containig a field
                        if letter == ";":
                            flag = 0
                            #Just the field value e.g. organism, age...
                            string_field = ""
                            for letter2 in field:
                                if letter2 == "[":
                                    flag = 1
                                if letter2 == "]":
                                    flag = 2
                                if flag == 1:
                                    string_field = string_field + letter2
                            #String with format to add column to the isa tab file e.g. Parameter Value[habitat]
                            string_add_column = field[:-1]
                            string_field = string_field[1:]
                            field = ""
                        #Check if there's no value for that field
                        #if string_field in fields_not_found:
                        if string_add_column in fields_not_found:
                            if letter == "\n":
                                keyword = keyword[:-1]
                                str =  "\\b{}\\b".format(keyword)
                                match = re.search(str, sentence, re.IGNORECASE)
                                #If the sentence has a keyword, add it to a dictionary of suggestions for that field
                                if match:
                                    if string_add_column in dict_suggestions:
                                        string_add = dict_suggestions[string_add_column]+sentence+"\n"
                                        dict_suggestions[string_add_column] = string_add
                                    else:
                                        dict_suggestions[string_add_column] = sentence+"\n"
                                keyword = ""
                                field = ""
                        else:
                            if letter =="\n":
                                keyword = ""
                                field = ""

                    sentence = ""

    return dict_suggestions

def add_extra_fields(dict_suggestions, study_file, file_name, fields_not_found, flag_factor_name, dict_factor_name, dict_sf_modified, no_suggestions):
    text=study_file
    text2=""
    add_count = 0
    dict_field_added = {}
    if not dict_suggestions:
        field = ""
        num_iteration = 0
        for letter in fields_not_found:
            field  = field + letter
            if letter == "\n":
                field = field[:-1]
                flag_units = 0
                unit = ""
                print("Would you like to add ", field, end= "")
                add_field = input("? (y/n)")
                if add_field == "y":
                    add_count += 1
                    line=0
                    value = input("Value:")
                    if "age" in field or "Duration" in field or "Temperature" in field or "Growth time" in field:
                        flag_units = 1
                        unit = input("Unit:")
                    text2= ""
                    for letter in text:
                        if letter == "\n":
                            if flag_units == 1:
                                dict_field_added[field] = value + "    Unit    "+ unit
                            else:
                                dict_field_added[field] =  value
                            if line ==0:
                                if flag_units == 1:
                                    text2 = text2 + "\u0009\u0022" +field+ "\u0022\u0009\u0022Unit\u0022\n"
                                else:
                                    text2 = text2 + "\u0009\u0022" +field+ "\u0022\n"
                                if flag_factor_name == 1:
                                    if num_iteration == 0:
                                        for key2 , values2 in dict_sf_modified.items():
                                            old = "\"Factor Value[" + values2[0] +"]\""
                                            new = "\"Factor Value[" + values2[1] + "]\""
                                            text2 = text2.replace(old, new)
                                line += 1
                            else:
                                if flag_units == 1:
                                    text2 = text2 + "\u0009\u0022"+value+"\u0022\u0009\u0022"+ unit + "\u0022\n"
                                else:
                                    text2 = text2 + "\u0009\u0022"+value+"\u0022\n"
                        else:
                            text2 = text2 + letter
                    text = text2
                    num_iteration += 1
                elif add_field != "y" and add_field != "n":
                    input("ERROR: Please enter a valid input.")
                field = ""
    else:
        num_iteration=0
        for key, values in dict_suggestions.items():
            flag_units = 0
            unit = ""
            print("\n\nThe following sentences may talk about", key, ":\n", values)
            add_field = input("Would you like to add a value? (y/n):")
            if add_field == "y":
                add_count += 1
                value = input("Value:")
                if "age" in key or "Duration" in key or "Temperature" in key or "Growth time" in key:
                    flag_units = 1
                    unit = input("Unit:")
                else:
                    flag_units = 0
                text2= ""
                line = 0
                for letter in text:
                    if letter == "\n":
                        if flag_units == 1:
                            dict_field_added[key] = value+ "   Unit    "+ unit
                        else:
                            dict_field_added[key] =  value
                        if line ==0:
                            if flag_units == 1:
                                text2 = text2 + "\u0009\u0022" +key + "\u0022\u0009\u0022Unit\u0022\n"
                            else:
                                text2 = text2 + "\u0009\u0022" +key + "\u0022\n"
                            if flag_factor_name == 1:
                                if num_iteration == 0:
                                    for key2 , values2 in dict_sf_modified.items():
                                        old = "\"Factor Value[" + values2[0] +"]\""
                                        new = "\"Factor Value[" + values2[1] + "]\""
                                        text2 = text2.replace(old, new)
                            line += 1
                        else:
                            if flag_units == 1:
                                text2 = text2 + "\u0009\u0022"+value+"\u0022\u0009\u0022" + unit +"\u0022\n"
                            else:
                                text2 = text2 + "\u0009\u0022"+value+"\u0022\n"
                    else:
                        text2 = text2 + letter
                text = text2
                num_iteration += 1
        field = ""
        for letter2 in no_suggestions:
            field = field + letter2
            if letter2 == "\n":
                field = field[:-1]
                add_field = input("There are no suggestions for: "+field+"Would you like to add it?(y/n)")
                if add_field == "y":
                    line=0
                    flag_units = 0
                    value = input("Value:")
                    if "age" in field or "Duration" in field or "Temperature" in field or "Growth time" in field:
                        flag_units = 1
                        unit = input("Unit:")
                    text2= ""
                    for letter in text:
                        if letter == "\n":
                            if flag_units == 1:
                                dict_field_added[field] = value+ "   Unit    "+ unit
                            else:
                                dict_field_added[field] =  value
                            if line ==0:
                                if flag_units == 1:
                                    text2 = text2 + "\u0009\u0022" +field+ "\u0022\u0009\u0022Unit\u0022\n"
                                else:
                                    text2 = text2 + "\u0009\u0022" +field[:-1]+ "\u0022\n"
                                if flag_factor_name == 1:
                                    if num_iteration == 0:
                                        for key2 , values2 in dict_sf_modified.items():
                                            old = "\"Factor Value[" + values2[0] +"]\""
                                            new = "\"Factor Value[" + values2[1] + "]\""
                                            text2 = text2.replace(old, new)
                                line += 1
                            else:
                                if flag_units == 1:
                                    text2 = text2 + "\u0009\u0022"+value+"\u0022\u0009\u0022"+ unit + "\u0022\n"
                                else:
                                    text2 = text2 + "\u0009\u0022"+value+"\u0022\n"
                        else:
                            text2 = text2 + letter
                        text = text2
                        num_iteration += 1
                field = ""

    #if no fields were added just change the factor name in header
    if add_count == 0:
        if flag_factor_name == 1:
            line_num=0
            header = ""
            for letter in text:
                if line_num==0:
                    header = header + letter
                if letter == "\n":
                    line_num += 1
            temp = header
            for key, values in dict_sf_modified.items():
                header2 = temp.replace(values[0], values[1])
                temp = header2
            text = text.replace(header, header2)

    return text, dict_field_added

def add_extra_fields_gui(dict_suggestions, study_file, file_name, fields_not_found, flag_factor_name, dict_factor_name, dict_sf_modified, no_suggestions, dict_fields_added):
    text=study_file
    text2=""
    add_count = 0

    num_line = 0
    line = ""
    for letter in text:
        line = line + letter
        if letter == "\n":
            if num_line == 0:
                for key, value in dict_fields_added.items():
                    line = line[:-1]
                    if "age" in key or "Duration" in key or "Temperature" in key or "Growth time" in key:
                        line = line + "\u0009\u0022"+key+"\u0022\u0009\u0022Unit\u0022\n"
                    else:
                        line = line + "\u0009\u0022"+key+"\u0022\n"
            else:
                for key, value in dict_fields_added.items():
                    line = line[:-1]
                    if "age" in key or "Duration" in key or "Temperature" in key or "Growth time" in key:
                        line = line + "\u0009\u0022"+value[0]+"\u0022\u0009\u0022"+value[1]+"\u0022\n"
                    else:
                        line = line + "\u0009\u0022"+value+"\u0022\n"
            text2 = text2 + line
            line = ""
            num_line += 1

    text = text2

    #Change the factor name in header
    if flag_factor_name == 1:
        line_num=0
        header = ""
        for letter in text:
            if line_num==0:
                header = header + letter
            if letter == "\n":
                line_num += 1
        temp = header
        for key, values in dict_sf_modified.items():
            header2 = temp.replace(values[0], values[1])
            temp = header2
        text = text.replace(header, header2)

    #Add fields to header

    return text


def generate_report(metadata_directory, GLDS_num, file_name_i, dict_dates_modified, dict_sf_modified, dict_field_added, file_name_s, dict_factor_name):

    file_name = "GLDS-"+GLDS_num+"_metadata_changes.txt"
    text = "GLDS-" + GLDS_num + ".\n INVESTIGATION FILE \n "
    text = text + "File modified: " + file_name_i + "\n\n Dates modified:\n"
    for key, values in dict_dates_modified.items():
        text = text + "    " + key + "      " + values[0] + "  -->  " + values[1] + "\n"
    text = text + "\n Study Factor Onthologies Modified:\n"
    for key, values in dict_sf_modified.items():
        text = text + "    " + key + "  -->  " + values[1] + "\n"

    cont = 0
    for key, values in dict_field_added.items():
        cont +=1

    text = text + "\n\n"
    text = text + " SAMPLE FILE\n"
    text = text + " File modified: " + file_name_s

    if cont > 0:
        text = text + "\n Fields added: \n"
        for key, values in dict_field_added.items():
            text = text + "    "+ key +"    " +values + "\n"
        text = text + "\n The following factor names were updated:\n"
        for key, values in dict_factor_name.items():
            text = text + "     "+values+"\n"
    else:
        text = text +"\n The following factor names were updated:\n"
        for key, values in dict_factor_name.items():
            text = text + "     "+values + "\n"
        text = text + "No new fields were added"

    f4 = open(os.path.join(metadata_directory, file_name), "w")
    f4.write(text)
    f4.close()


# while True:
#     try:
#         #Metadata folder directory
#         os.system('clear')
#         print("METADATA NORMALIZATION \n Enter 'exit' to leave...")
#         metadata_directory = input("Name of the metadata directory: ")
#         if metadata_directory == "exit":
#             break;
#         outdir = input("Name of the output directory:")
#         if outdir == "exit":
#             break;
#         GLDS_num = clean(metadata_directory, outdir)
#     except Exception as e:
#         print(e, "\nPress enter to try another directory...")
#         input()
#     else:
def norm(metadata_directory, outdir, GLDS_num):
        os.system('clear')
        print("METADATA NORMALIZATION\n\n")

        print("Metadata for GLDS-", GLDS_num)

        #PROJECT_ROOT = os.path.dirname((os.path.abspath(__file__)))
        #for root, dirs, files in os.walk(PROJECT_ROOT+"/metadata", topdown=True):
        [study_type, organism]=find_study_type(GLDS_num)
        print("Organism type: ", study_type)

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

        add_files_flag = input("\nWould you like to add the missing fields? (y/n):")
        if add_files_flag == "y":
            dict_suggestions = {}
            dict_suggestions = find_seuggestions(keywords_file, fields_not_found)
            no_suggestions =""
            field =""
            for letter in fields_not_found:
                field = field + letter
                if letter == "\n":
                    field = field[:-1]
                    if field not in dict_suggestions:
                        no_suggestions = no_suggestions + field + "\n"
                    field = ""

            [norm_sample_file, dict_field_added] = add_extra_fields(dict_suggestions, study_file, file_name_s, fields_not_found, flag_factor_name, dict_factor_name, dict_sf_modified, no_suggestions)
            #f4 = open(os.path.join(metadata_directory, file_name_s), "w")
            f4 = open(os.path.join(outdir, file_name_s), "w+")
            f4.write(norm_sample_file)
            f4.close()

            generate_report(metadata_directory, str(GLDS_num), file_name_i, dict_dates_modified, dict_sf_modified, dict_field_added, file_name_s, dict_factor_name)
            input("Investigation and Sample files were normalized.\nPress enter to continue")
        elif add_files_flag == "n":
            print("Investigation file was normalized.\n No new fields were added to the Sample File.")
            #Change facrtor name in study file
            if flag_factor_name == 1:
                line_num=0
                header = ""
                for letter in study_file:
                    if line_num==0:
                        header = header + letter
                    if letter == "\n":
                        line_num += 1
                temp = header
                for key, values in dict_sf_modified.items():
                    header2 = temp.replace(values[0], values[1])
                    temp = header2
                dict_field_added={}

                study_file = study_file.replace(header, header2)
                #f4 = open(os.path.join(metadata_directory, file_name_s), "w")
                f4 = open(os.path.join(outdir, file_name_s), "w+")
                f4.write(study_file)
                f4.close()
            else:
                dict_field_added = {}

            generate_report(metadata_directory, str(GLDS_num), file_name_i, dict_dates_modified, dict_sf_modified, dict_field_added, file_name_s, dict_factor_name)
            input("Press enter to continue")
            #sys.exit()
        elif add_files_flag == "exit":
            sys.exit()
        else:
            print("Please enter a valid option or 'exit' to leave...")
