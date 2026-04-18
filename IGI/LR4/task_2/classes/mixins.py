import os
import zipfile

class FileMixin():

    def save_into_file(self, data, filename="filename.txt"):
        "Save data into file"
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(data)

    def archive(self, filename="filename.txt", zipfilename="my_zipfile.zip"):
        """Archive data by filename and archivename"""
        with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as f:
            filename_only = os.path.basename(filename)
            f.write(filename, arcname=filename_only) 

    def get_info_zip(self, zipfilename="my_zipfile.zip"):
        """Get info about archive"""

        if not os.path.exists(zipfilename):
            print("No found this archive")
            return
        with zipfile.ZipFile(zipfilename, 'r') as f:
            for info in f.infolist():
                print(f"File into archive: {info.filename}")
                print(f"Orig size: {info.file_size}") 
                print(f"Zip size: {info.compress_size}")  
                print(f"Time: {info.date_time}")     