import os
import zipfile
import datetime
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
        inform = []
        if not os.path.exists(zipfilename):
            print("No found this archive")
            return
        with zipfile.ZipFile(zipfilename, 'r') as f:
            for info in f.infolist():
                smth = f"File into archive: {info.filename}"
                print(smth)
                inform.append(smth) 

                smth = f"Orig size: {info.file_size}"
                print(smth)
                inform.append(smth)

                smth = f"Zip size: {info.compress_size}"
                print(smth)
                inform.append(smth)

                date =  datetime.datetime(*info.date_time)
                smth = f"Time: {date.strftime('%d.%m.%Y %H:%M:%S')}"
                print(smth)
                inform.append(smth)
        return inform

                  