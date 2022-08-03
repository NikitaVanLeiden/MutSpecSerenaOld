import csv
from os import listdir, rename, makedirs
from os.path import isfile, join, exists

# Path to the table with ID and agent names
file_names_table_path = '/Users/Nikita Neumann/Desktop/Study/MutSpecSerena-master//body/1raw/treatment_mapped_to_kostya_files.csv'
# Path to the folder with file that shoud to be renamed
files_to_rename_path = '/Users/Nikita Neumann/Desktop/Study/MutSpecSerena-master/body/1raw/MtMutectAnnovar/'
# Folder with renamed files
folder_with_renamed_files = '/Users/Nikita Neumann/Desktop/Study/MutSpecSerena-master/body/1raw/MtMutectAnnovar/renamed/'
# Result file name
result_file_name = '/Users/Nikita Neumann/Desktop/Study/MutSpecSerena-master/result.csv'

def get_filenames_dict(path):
    """
    This method get IDs and agent's name to the dictionary.
    :param path:
    :return: agent_names_dict
    """
    agent_names_dict = {}  # Create a dictionary with ID and agent names
    with open(path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            if row["treatment"]:  # Check if agent name exist
                agent_names_dict.update({row["filename"]: row["treatment"]})  # add ID and agent name to the dict.
        return agent_names_dict

def get_file_names(path):
    list_of_file_names = [f for f in listdir(path) if isfile(join(path, f))]
    return list_of_file_names

def get_first_part_from_file_name(file_name):
    id = file_name.split(".")[0]
    return id

def create_folder_with_renamed_files_if_not_exists(directory):
    if not exists(directory):
        makedirs(directory)

def rename_files(files_to_rename_path, file_names_table_path):
    list_of_file_names = get_file_names(files_to_rename_path)
    file_names_dict = get_filenames_dict(file_names_table_path)
    create_folder_with_renamed_files_if_not_exists(folder_with_renamed_files)
    for file in list_of_file_names:
        id = get_first_part_from_file_name(file)
        if id in file_names_dict:
            new_file_name = file_names_dict[id] + "." + file
            rename(files_to_rename_path + file, folder_with_renamed_files + new_file_name)
    return

def count_file(file):
    full_file_name = folder_with_renamed_files + file
    file_count_dict = {
    "agent_name": get_first_part_from_file_name(file),
    "AT": 0,
    "AG": 0,
    "AC": 0,
    "CT": 0,
    "CA": 0,
    "CG": 0,
    "TC": 0,
    "TA": 0,
    "TG": 0,
    "GA": 0,
    "GT": 0,
    "GC": 0
    }
    with open(full_file_name, mode='r') as csv_source:
        csv_reader = csv.DictReader(csv_source, delimiter='\t', fieldnames=[0, 1, 2, 3, 4, 5, 6])
        for row in csv_reader:
            if row[3] + row[4] in file_count_dict:
                file_count_dict[row[3] + row[4]] += 1
    return file_count_dict

def change_count(path):
    result = []
    renamed_files = get_file_names(path)
    for file in renamed_files:
        if file.endswith(".Vcf4"):
            file_count_dict = count_file(file)  # dict with mutation count
            result.append(file_count_dict)
    return result

def combine_two_dict(dict1, dict2):
    res_dict = dict2.copy()
    for key in dict2:
        if key in dict1:
            res_dict[key] = dict2[key] + dict1[key]
        else:
            pass
    return res_dict

def get_set_of_result_agents(result):
    agents_set = set()
    for row in result:
        agents_set.add(row["agent_name"])
    return agents_set

def result_deduplication(result):
    deduplicated_result = []
    agent_names_set = get_set_of_result_agents(result)
    for i in agent_names_set:
        sum = {}
        for j in result:
            if i == j["agent_name"]:
                sum = combine_two_dict(sum, j)  # get sum of two rows with the same agent name
                sum["agent_name"] = j["agent_name"]  # set correct (not duplicated) agent name
        deduplicated_result.append(sum)
    return deduplicated_result

def save_result_to_file(deduplicated_result, result_file_name):
    with open(result_file_name, mode='w+') as csv_file:
        fieldnames = ["agent", "AT", "AG", "AC", "CT", "CA", "CG", "TC", "TA", "TG", "GA", "GT", "GC"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for file in deduplicated_result:
            writer.writerow({
                "agent": file["agent_name"],
                "AT": file["AT"],
                "AG": file["AG"],
                "AC": file["AC"],
                "CT": file["CT"],
                "CA": file["CA"],
                "CG": file["CG"],
                "TC": file["TC"],
                "TA": file["TA"],
                "TG": file["TG"],
                "GA": file["GA"],
                "GT": file["GT"],
                "GC": file["GC"]
            })


if __name__ == '__main__':
    rename_files(files_to_rename_path, file_names_table_path)
    result = change_count(folder_with_renamed_files)
    deduplicated_results = result_deduplication(result)
    save_result_to_file(deduplicated_results, result_file_name)