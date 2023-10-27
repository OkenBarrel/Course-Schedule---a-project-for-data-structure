import os

def check_dir(dir_path,file_path):
    entries=os.listdir(dir_path)
    if '/' in file_path:
        file=file_path.split('/')
        print(file)
        file_name=file[-1]
        print(file_name)
    else:               #file_path is a name instead of a path
        file_name=file_path
        print(file_name)
    if file_name in entries:
        return True
    else:
        return False


# print(check_dir('E:/Files for Work/ds proj/courseSchedule/views','E:/Files for Work/ds proj/courseSchedule/views/v.png'))