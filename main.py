import os
import shutil
import hashlib
import sys
import logging
import keyboard
import time
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")


def delete_excessive_files(source, destination):
    list_of_files_delete = os.listdir(dst)
    # iterate over each element in list
    for j in list_of_files_delete:
        dst1 = destination + "\\" + j
        src1 = source + "\\" + j
        logging.warning("Source " + src1)
        # check if the file at the path exists
        if not os.path.isfile(src1):
            os.remove(dst1)
            logging.warning("The " + dst1 + " file in replica folder was deleted")
            print("\nThe " + dst1 + " file in replica folder was deleted.")


def compare2files_by_hash(file_from_src, file_from_dst):
    # Version for small files hashing:
    # with open(src2, "rb") as file:
    #     bytes = file.read()
    #     print ("Bytes: ", bytes)
    #     result = hashlib.md5(bytes)
    #     print("Hash value: ", result)
    #     print("Hexadecimal: ", result.hexdigest())
    chunks = 1024
    md5hash = hashlib.md5()
    with open(file_from_src, "rb") as f:
        cbytes = -1
        while cbytes != b'':
            cbytes = f.read(chunks)
            md5hash.update(cbytes)
    logging.debug('1Hash value:  {}'.format(md5hash))
    file_from_src_hash = md5hash.hexdigest()
    logging.debug('1Hexadecimal:  {}'.format(file_from_src_hash))
    md5hash2 = hashlib.md5()
    with open(file_from_dst, "rb") as f2:
        cbytes2 = -1
        while cbytes2 != b'':
            cbytes2 = f2.read(chunks)
            md5hash2.update(cbytes2)
    logging.debug('2Hash value:  {}'.format(md5hash2))
    file_from_dst_hash = md5hash2.hexdigest()
    logging.debug('2Hexadecimal:  {}'.format(file_from_dst_hash))
    return file_from_src_hash == file_from_dst_hash


# Option for manual input of the log path
# src = "C:\All\Test_Python_Veeam_PyCh\Source_folder"
# dst = "C:\All\Test_Python_Veeam_PyCh\Replica_folder"

# total arguments
length_of_array = len(sys.argv)
print("\nTotal arguments passed:", length_of_array)

if length_of_array != 5:
    print("\nThere are too many arguments or not enough, please, start from the beginning")
    print("\nThe arguments should be following:")
    print("\n1. Name of Python script")
    print("\n2. Path to source folder")
    print("\n3. Path to destination (replica) folder")
    print("\n4. Path for log file creation")
    print("\n5. Synchronization interval in seconds")
else:
    # Option for manual input of the log path
    # path_to_log = "C:\All\Job\pythontest\\"
    src = sys.argv[1]
    dst = sys.argv[2]
    path_to_log = sys.argv[3]
    synch_interval = int(sys.argv[4])
    logging.basicConfig(filename=path_to_log + dt_string + "log.txt", level=logging.DEBUG,
                        format="%(asctime)s %(message)s")
    logging.warning("The log file was created")
    print("\nThe log file was created")
    print("\nYou are trying to start synchronization ")
    print("of files from " + src + " folder to " + dst + " folder \nwith interval of " + sys.argv[4] + " seconds")
    print("\nWas every argument provided correctly? Press 'y' key to proceed or any other key to stop the script")

    if keyboard.read_key() == "y":
        print("\nYou pressed 'y'. To stop the script press 'Ctrl+c'.")
        try:
            while True:
                list_of_files = os.listdir(src)
                logging.debug(list_of_files)
                # Deletion of the excessive files in destination folder
                delete_excessive_files(src, dst)
                # iterate over each element in list
                for i in list_of_files:
                    print("\nName of file ", "is: ", i)
                    logging.warning("Name of file " + "is: " + i)
                    dst2 = dst + "\\" + i
                    print(dst2)
                    logging.warning("Destination " + dst2)
                    src2 = src + "\\" + i
                    print(src2)
                    logging.warning("Source " + src2)
                    # check if the file at the path exists
                    if os.path.isfile(dst2):
                        result_of_compare = compare2files_by_hash(src2, dst2)
                        if not result_of_compare:
                            shutil.copyfile(src2, dst2)
                            logging.warning("The file in replica folder was replaced with the file from source folder")
                            print("\nThe files have the same name, but different content.")
                            print("\nSo the file in replica folder was replaced with the file from source folder")
                            # print("\nTo stop the script press 'Ctrl+c'.")
                        else:
                            logging.warning("The files are the same, so the copying was not carried out")
                            print("\nThe files are the same, so the copying was not carried out")
                            # print("\nTo stop the script press 'Ctrl+c'.")
                    else:
                        shutil.copyfile(src2, dst2)
                        logging.warning("\nThe file was copied from the source folder to the replica folder")
                        print("\nThe file does not exist in destination folder, so it was copied")
                        # print("\nTo stop the script press 'Ctrl+c'.")
                print("\nTo stop the script press 'Ctrl+c'.")
                time.sleep(synch_interval)
        except KeyboardInterrupt:
            logging.warning("The script was stopped by user")
            print("\nThe script was stopped")
            pass
    else:
        logging.warning("The script was stopped by user")
        print("\nThe script was stopped")
        sys.exit()
