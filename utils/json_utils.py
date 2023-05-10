import json

def jsonfile_get_data(file_name):
    with open(file_name,'r') as file:
        file_data = json.load(file)
        file.close()
    return file_data

def jsonfile_save_data(file_name, file_data):
    with open(file_name,'w') as file:
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4, sort_keys=True)
        file.close()

