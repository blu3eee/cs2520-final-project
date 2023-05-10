import json

def add_list_json(
    file_name: str, 
    list_name: str, 
    value
) -> bool:
    # open json file to read file_data
    with open(file_name,'r') as file:
        file_data = json.load(file)
        file.close()
    # modify
    if list_name not in file_data:
        file_data[list_name] = []
    if value in file_data[list_name]:
        return False # return false if already in the list
    # append if valid
    file_data[list_name].append(value)
    # update json file
    with open(file_name,'w') as file:
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
        file.close()
    return True

def add_list_json_rcrsv(
    file_data, 
    list_name, 
    value
) -> bool:
    if len(list_name) == 1:
        # modify
        if list_name not in file_data:
            file_data[list_name] = []
        if value in file_data[list_name]:
            return False # return false if already in the list
        # append if valid
        file_data[list_name].append(value)
        
        return file_data
    file_data[list_name[0]] = add_list_json_rcrsv(file_data[list_name[0]], list_name[1:], value)
    return file_data

def remove_list_json(
    file_name: str, 
    list_name: str, 
    value
) -> bool:
    # open json file to read file_data
    with open(file_name,'r') as file:
        file_data = json.load(file)
        file.close()
    # modify
    if list_name not in file_data:
        return False # return false if list not exist
    if value not in file_data[list_name]:
        return False # return false if already in the list
    # remove if valid
    file_data[list_name].remove(value)
    # update json file
    with open(file_name,'w') as file:
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4, sort_keys=True)
        file.close()
    return True


        