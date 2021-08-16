import package1
import app_logger
import xml.etree.ElementTree as ET
import threading
import os
import shutil
import time
from tqdm import tqdm
from pathlib import Path


logger = app_logger.get_logger(__name__)
CHECK = False

def parse_config():
    while True:
        try:
            tree = ET.parse("config_file.xml")
            root = tree.getroot()

            for files in tqdm(root):
                time.sleep(1)
                source_path = files.get("source_path")
                destination_path = files.get("destination_path")
                file_name = files.get("file_name")
                num_files = len(root)
                copy_file(source_path, destination_path, file_name, num_files )
            return False
        except FileNotFoundError:
            pass
            logger.warning("Can not find the config")
            return False        
            
def copy_file(source, destination, file_name, num_files):
    source_path = os.path.abspath(source.replace("\\", "/"))
    destination_path = os.path.abspath(destination.replace("\\", "/"))
    
    try:
        valid_open = open(os.path.join(source_path, file_name) , mode="r")
        valid_open.close()
    except FileNotFoundError:
        logger.warning("Can not find the file ", file_name)
        return False
    
    if (os.path.exists(os.path.join(destination_path, file_name))) == False:
        try:
            shutil.copy(os.path.join(source_path, file_name), os.path.join(destination, file_name))
            time.sleep(1)
            logger.info("File " + file_name + " copied successfully.")
        
        except shutil.SameFileError:
            logger.warning("Source and destination represents the same file" + file_name)
            return False

        except IOError:
            logger.warning("File" + file_name+ " is not read.")
            return False
        
        except PermissionError:
            logger.warning(file_name + "Permission denied.")
            return False
         
        except:
            logger.warning(" Error occurred while copying file" + file_name)
        
    else:
        try:
            command = input('The file already exists at the you want to overwrite the package at destination? Y/N/R(Rename): ')
            if command == "Y":
                os.remove(os.path.join(destination_path, file_name))
                shutil.copy(os.path.join(source_path, file_name), os.path.join(destination, file_name))
                logger.info("File " + file_name + " overwritten.")
        
            if command == "R":
                new_file_name = input('Enter a new filename: ')
                valid_name = False
                if os.path.exists(os.path.join(destination_path, new_file_name + Path(os.path.join(destination, file_name)).suffix)) == True:        
                    while valid_name == False:
                        new_file_name = input('A file with the same name already exists in the folder. Please enter a different filename: ')
                        if (os.path.exists(os.path.join(destination_path, new_file_name + Path(os.path.join(destination, file_name)).suffix))) == False:
                            valid_name = True
                    shutil.copy(os.path.join(source_path, file_name), os.path.join(destination, new_file_name) + Path(os.path.join(destination, file_name)).suffix)
                    logger.info("File " + new_file_name + Path(os.path.join(destination, file_name)).suffix + " copied successfully.")
                    return False
                else:
                    shutil.copy(os.path.join(source_path, file_name), os.path.join(destination, new_file_name) + Path(os.path.join(destination, file_name)).suffix)
                    logger.info("File " + new_file_name + Path(os.path.join(destination, file_name)).suffix + " copied successfully.")
                    return False
            else:
                return 
        except:
            logger.warning("Error occurred while copying file.")

if __name__ == "__main__":
    thread = threading.Thread(target=parse_config)
    thread.start()
