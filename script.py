import datetime
import sys
import zipfile
import psutil
import os


def bytes_to_gb(bytes):
    return bytes / (1024 ** 3)


def print_drive_sizes():
    drives = [drive.mountpoint for drive in psutil.disk_partitions()]

    for drive in drives:
        print(f"Drive \"{drive}\":\n"
              f"{round(bytes_to_gb(psutil.disk_usage(drive).used), 2)}/"
              f"{round(bytes_to_gb(psutil.disk_usage(drive).total), 2)} Gb used")


def get_zip_filename():
    datetime_now = datetime.datetime.now()
    datetime_filename = datetime_now.strftime("%m.%d.%Y,%H:%M:%S")
    return f"{datetime_filename}.zip"


def folder_backup_to_zip(path="/home/somename/work"):
    abs_path = os.path.abspath(path)
    file_name = f"/tmp/{get_zip_filename()}"
    backup_zip = zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED)
    for foldername, subfolders, filenames in os.walk(abs_path):
        for filename in filenames:
            absname = os.path.abspath(os.path.join(foldername, filename))
            arcname = absname[len(abs_path) + 1:]
            # print(f"Zipping {os.path.join(foldername, filename)} as {arcname}")
            backup_zip.write(absname, arcname=arcname)
    print("Backup complete")


def get_file_size(path):
    size = os.path.getsize(path)
    return size


def delete_big_files(folder="/tmp/", size=1024**3):
    for foldername, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            filesize = get_file_size(file_path)
            if filesize > size:
                print(f"{os.path.abspath(file_path)} - {round(bytes_to_gb(filesize), 2)} Gb")
                print(f"File {filename} deleted")
                # os.remove(file_path)  # be careful


if __name__ == "__main__":
    argv_len = len(sys.argv)

    if argv_len == 1:
        print_drive_sizes()
        folder_backup_to_zip()
        delete_big_files()

    elif argv_len > 1:
        if sys.argv[1] == "--help":
            print("--drives                 - List of drives sizes.\n"
                  "--backup <directory>     - Backups the specified directory and its content recursively in /tmp/. "
                  "/home/somename/work - by default.\n"
                  "--big <directory> <size> - Finds and removes files bigger than a specific size in bytes in directory"
                  " recursively. Flags defined together only. 1 Gb files in /tmp/ directory by default.\n")

        if sys.argv[1] == "--drives":
            print_drive_sizes()

        if sys.argv[1] == "--backup":
            if argv_len > 2:
                directory = sys.argv[2]
                folder_backup_to_zip(path=directory)
            else:
                folder_backup_to_zip()

        if sys.argv[1] == "--big":
            if argv_len > 2:
                directory = sys.argv[2]
                size = int(sys.argv[3])
                delete_big_files(directory, size)
            else:
                delete_big_files()
