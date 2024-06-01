import os
import shutil

def copy_directory_contents(source_directory_path, destination_directory_path):
    source_directory_path = os.path.abspath(source_directory_path)
    destination_directory_path = os.path.abspath(destination_directory_path)

    print(f"Source Path: {source_directory_path}")
    print(f"Destination Path: {destination_directory_path}")
    
    if not os.path.exists(source_directory_path):
        raise ValueError(f"Invalid source directory path: {source_directory_path}. Please make sure the path exists.")
    if not os.path.exists(destination_directory_path):
        try:
            os.mkdir(destination_directory_path)
        except Exception as e:
            print(f"Error: {str(e)} | Destination path did not exist, but also could not be created. Check to make sure there aren't errors in the destination_directory_path.")
    else:
        shutil.rmtree(destination_directory_path)
        os.mkdir(destination_directory_path)

    source_contents = os.listdir(source_directory_path)
    
    for file in source_contents:
        source_file_path = os.path.join(source_directory_path, file)
        destination_file_path = os.path.join(destination_directory_path, file)

        if os.path.isdir(source_file_path):
            print(f"{file} is a directory, recursing...")
            copy_directory_contents(source_file_path, destination_file_path)
        else:
            print(f"Copying {source_file_path}")
            shutil.copy(source_file_path, destination_file_path)
            print(f"File {file} copied from {source_file_path} to {destination_file_path}")
        